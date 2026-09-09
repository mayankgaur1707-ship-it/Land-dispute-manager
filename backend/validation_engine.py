import uuid
import json
import math
from typing import List, Dict, Any, Tuple
from shapely.geometry import shape, mapping, Polygon
from shapely.validation import make_valid
from backend.models import DisputeType, DisputeStatus
from backend.database import get_all_records, save_dispute

# Geodetic conversion approximation for northern India (latitude ~26-28 deg)
METERS_PER_DEG_LAT = 111132.0
METERS_PER_DEG_LON = 98000.0

def polygon_area_sq_meters(poly: Polygon) -> float:
    """Calculates approximate metric area of a polygon in WGS84 coordinates."""
    # Transform coordinates from lon/lat degrees to approximate meters
    coords = list(poly.exterior.coords)
    if len(coords) < 3:
        return 0.0
    # Shoelace formula on projected meter coordinates
    n = len(coords)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        xi, yi = coords[i][0] * METERS_PER_DEG_LON, coords[i][1] * METERS_PER_DEG_LAT
        xj, yj = coords[j][0] * METERS_PER_DEG_LON, coords[j][1] * METERS_PER_DEG_LAT
        area += (xi * yj) - (xj * yi)
    return abs(area) / 2.0

def validate_land_record(candidate: Dict[str, Any], existing_records: List[Dict[str, Any]] = None) -> Tuple[str, List[str], List[Dict[str, Any]], float, str]:
    """
    Validates a land record against existing records and rule-based checks.
    Returns:
      - dispute_status: 'CLEAR', 'WARNING', or 'DISPUTED'
      - dispute_tags: List of descriptive tags
      - created_disputes: List of DisputeRecord dicts to persist
      - confidence_score: float (0.0 to 1.0)
    """
    if existing_records is None:
        existing_records = get_all_records()
        
    dispute_tags = []
    created_disputes = []
    confidence = 1.0
    status = DisputeStatus.CLEAR

    candidate_id = candidate.get("id") or str(uuid.uuid4())
    khasra_no = candidate.get("khasra_no", "").strip()
    village = candidate.get("village", "").strip().lower()
    owners = candidate.get("owners", [])
    stated_area = candidate.get("area_sq_meters", 0.0)

    # 1. Share Mismatch Validation
    total_shares = sum(o.get("share_percentage", 0.0) for o in owners)
    if abs(total_shares - 100.0) > 0.01:
        dispute_tags.append(f"Share mismatch: Owner shares sum to {total_shares:.1f}% instead of 100%")
        confidence -= 0.25
        status = DisputeStatus.WARNING
        created_disputes.append({
            "id": f"DISP-{uuid.uuid4().hex[:8].upper()}",
            "record_ids": [candidate_id],
            "dispute_type": DisputeType.OWNERSHIP_SHARE_MISMATCH.value,
            "title": f"Co-sharer Equity Imbalance (Khasra {khasra_no})",
            "description": f"The combined ownership percentage across declared co-sharers is {total_shares:.1f}%, violating statutory 100% full-title closure.",
            "overlap_geojson": None,
            "overlap_area_sq_meters": None,
            "severity": "MEDIUM",
            "status": "ACTIVE",
            "resolution_notes": None,
            "created_at": candidate.get("created_at", "")
        })

    # 2. Duplicate Survey / Khasra Number Detection
    for existing in existing_records:
        if existing["id"] == candidate_id:
            continue
        if existing.get("khasra_no", "").strip() == khasra_no and existing.get("village", "").strip().lower() == village:
            dispute_tags.append(f"Duplicate Khasra #{khasra_no} detected in {candidate.get('village')}")
            confidence -= 0.4
            status = DisputeStatus.DISPUTED
            created_disputes.append({
                "id": f"DISP-{uuid.uuid4().hex[:8].upper()}",
                "record_ids": [candidate_id, existing["id"]],
                "dispute_type": DisputeType.DUPLICATE_SURVEY_NO.value,
                "title": f"Duplicate Khasra Title Claim: #{khasra_no}",
                "description": f"Khasra number {khasra_no} is already registered under ID {existing['id']} to owner(s): {', '.join(o['name'] for o in existing.get('owners', []))}. Potential double-registration or contested sale.",
                "overlap_geojson": None,
                "overlap_area_sq_meters": None,
                "severity": "CRITICAL",
                "status": "ACTIVE",
                "resolution_notes": None,
                "created_at": candidate.get("created_at", "")
            })

    # 3. Spatial Boundary Overlap / Encroachment Detection (GIS Shapely)
    candidate_geom_data = candidate.get("boundary_geojson")
    if candidate_geom_data:
        try:
            cand_shape = shape(candidate_geom_data)
            if not cand_shape.is_valid:
                cand_shape = make_valid(cand_shape)

            calculated_area = polygon_area_sq_meters(cand_shape)

            # Check area discrepancy vs stated area
            if stated_area > 0 and calculated_area > 0:
                area_ratio = abs(calculated_area - stated_area) / max(stated_area, 1.0)
                if area_ratio > 0.30:  # > 30% difference between boundary geometry and deed text
                    dispute_tags.append(f"Area variance: Boundary polygon ({calculated_area:.1f} m²) differs from deed ({stated_area:.1f} m²)")
                    confidence -= 0.15

            # Test spatial overlap with all existing parcels
            for existing in existing_records:
                if existing["id"] == candidate_id:
                    continue
                ex_geom_data = existing.get("boundary_geojson")
                if not ex_geom_data:
                    continue
                try:
                    ex_shape = shape(ex_geom_data)
                    if not ex_shape.is_valid:
                        ex_shape = make_valid(ex_shape)
                    
                    if cand_shape.intersects(ex_shape):
                        intersection = cand_shape.intersection(ex_shape)
                        # Filter out point or line-touch boundaries (only real polygon overlaps)
                        if intersection.area > 1e-9:
                            overlap_sqm = polygon_area_sq_meters(intersection)
                            if overlap_sqm >= 1.0:  # More than 1 square meter overlap
                                overlap_geojson = mapping(intersection)
                                status = DisputeStatus.DISPUTED
                                confidence -= 0.45
                                dispute_tags.append(f"Spatial Encroachment: Overlaps {overlap_sqm:.1f} m² with Khasra #{existing['khasra_no']}")
                                
                                created_disputes.append({
                                    "id": f"DISP-{uuid.uuid4().hex[:8].upper()}",
                                    "record_ids": [candidate_id, existing["id"]],
                                    "dispute_type": DisputeType.BOUNDARY_OVERLAP.value,
                                    "title": f"Cadastral Boundary Encroachment: #{khasra_no} vs #{existing['khasra_no']}",
                                    "description": f"Parcel #{khasra_no} encroaches upon parcel #{existing['khasra_no']} by approximately {overlap_sqm:.2f} sq. meters. Immediate physical demarcator review required.",
                                    "overlap_geojson": overlap_geojson,
                                    "overlap_area_sq_meters": round(overlap_sqm, 2),
                                    "severity": "CRITICAL" if overlap_sqm > 50 else "HIGH",
                                    "status": "ACTIVE",
                                    "resolution_notes": None,
                                    "created_at": candidate.get("created_at", "")
                                })
                except Exception as e:
                    print(f"Error checking polygon intersection: {e}")
        except Exception as e:
            dispute_tags.append(f"Invalid boundary geometry: {e}")
            confidence -= 0.3
            status = DisputeStatus.WARNING

    # 4. Field-level Confidence & Human-in-the-Loop Flagging
    field_confidences = candidate.get("field_confidences", {})
    has_low_confidence_field = False
    verification_status = candidate.get("verification_status") or "AUTO_VERIFIED"

    for f_name, f_data in field_confidences.items():
        conf_val = f_data.get("confidence", 1.0) if isinstance(f_data, dict) else getattr(f_data, "confidence", 1.0)
        is_low = f_data.get("is_low_confidence", False) if isinstance(f_data, dict) else getattr(f_data, "is_low_confidence", False)
        if is_low or conf_val < 0.85:
            has_low_confidence_field = True
            dispute_tags.append(f"Uncertain OCR: Field '{f_name}' confidence {int(conf_val*100)}% requires manual review")
            confidence = min(confidence, conf_val)

    if has_low_confidence_field and verification_status != "VERIFIED_BY_OFFICER":
        verification_status = "PENDING_VERIFICATION"
        if status == DisputeStatus.CLEAR:
            status = DisputeStatus.WARNING

    confidence = max(0.05, min(1.0, round(confidence, 2)))
    if status == DisputeStatus.CLEAR and dispute_tags:
        status = DisputeStatus.WARNING

    return status.value, dispute_tags, created_disputes, confidence, verification_status
