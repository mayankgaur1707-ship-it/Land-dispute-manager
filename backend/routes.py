import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Body
from fastapi.responses import Response

from backend.models import (
    LandRecordCreate, LandRecord, DisputeRecord,
    DisputeStatus, DisputeType, VerificationStatus, HumanVerificationSubmission
)
from backend.database import (
    get_all_records, get_record_by_id, save_record,
    get_all_disputes, save_dispute, update_dispute_status,
    get_audit_ledger, get_pending_verifications, get_state_district_analytics
)
from backend.validation_engine import validate_land_record
from backend.ocr_service import extract_land_record_from_text, get_sample_templates, generate_document_svg, SAMPLE_TEMPLATES
from backend.blockchain_audit import record_audit_event, verify_audit_ledger, calculate_sha256

router = APIRouter(prefix="/api")

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Intelligent Land Record Digitization and Validation API",
        "version": "1.0.0",
        "dilrmp_integrated": True,
        "gis_engine": "Shapely WGS84 Geodetic",
        "blockchain_audit": "SHA-256 Chained Ledger"
    }

@router.get("/analytics")
def get_analytics():
    records = get_all_records()
    disputes = get_all_disputes()
    
    total_records = len(records)
    clear_count = sum(1 for r in records if r.get("dispute_status") == DisputeStatus.CLEAR.value)
    warning_count = sum(1 for r in records if r.get("dispute_status") == DisputeStatus.WARNING.value)
    disputed_count = sum(1 for r in records if r.get("dispute_status") == DisputeStatus.DISPUTED.value)
    
    pending_verification_count = sum(1 for r in records if r.get("verification_status") == VerificationStatus.PENDING_VERIFICATION.value)
    auto_verified_count = sum(1 for r in records if r.get("verification_status") == VerificationStatus.AUTO_VERIFIED.value)
    officer_verified_count = sum(1 for r in records if r.get("verification_status") == VerificationStatus.VERIFIED_BY_OFFICER.value)

    active_disputes = [d for d in disputes if d["status"] == "ACTIVE"]
    resolved_disputes = [d for d in disputes if d["status"] == "RESOLVED"]
    
    total_area_hectares = sum(r.get("area_hectares", 0.0) for r in records)
    avg_confidence = (sum(r.get("confidence_score", 1.0) for r in records) / total_records) if total_records > 0 else 1.0

    state_data = get_state_district_analytics()

    return {
        "total_records": total_records,
        "clear_records": clear_count,
        "warning_records": warning_count,
        "disputed_records": disputed_count,
        "pending_verifications": pending_verification_count,
        "auto_verified_count": auto_verified_count,
        "officer_verified_count": officer_verified_count,
        "active_disputes": len(active_disputes),
        "resolved_disputes": len(resolved_disputes),
        "total_area_hectares": round(total_area_hectares, 2),
        "avg_confidence_score": round(avg_confidence * 100, 1),
        "villages": list(set(r.get("village", "") for r in records)),
        "state_breakdown": state_data.get("states", {}),
        "district_breakdown": state_data.get("districts", {})
    }

@router.get("/analytics/progress")
def get_progress():
    return get_state_district_analytics()

@router.get("/templates")
def list_templates():
    return get_sample_templates()

@router.get("/templates/{template_id}/document-svg")
def get_template_document_svg(template_id: str):
    tpl = SAMPLE_TEMPLATES.get(template_id)
    if not tpl:
        raise HTTPException(status_code=404, detail="Template not found")
    data = dict(tpl["parsed"])
    data["language"] = tpl.get("language", "Hindi (हिंदी)")
    data["document_type"] = tpl.get("document_type", "Scanned PDF / Khasra")
    svg_content = generate_document_svg(data)
    return Response(content=svg_content, media_type="image/svg+xml")

@router.get("/records/")
def list_records(
    search: Optional[str] = None,
    status: Optional[str] = None,
    village: Optional[str] = None,
    verification: Optional[str] = None
):
    records = get_all_records()
    filtered = []
    for r in records:
        if status and r.get("dispute_status") != status:
            continue
        if verification and r.get("verification_status") != verification:
            continue
        if village and r.get("village", "").lower() != village.lower():
            continue
        if search:
            s = search.lower()
            owners_str = " ".join(o["name"].lower() for o in r.get("owners", []))
            if (s not in r.get("khasra_no", "").lower() and
                s not in r.get("khata_no", "").lower() and
                s not in r.get("village", "").lower() and
                s not in owners_str):
                continue
        filtered.append(r)
    return filtered

@router.get("/records/pending-verification")
def list_pending_verifications():
    """
    Returns the Human-in-the-Loop verification queue for Revenue Officers / Patwaris.
    Lists records where AI-OCR confidence on any critical field was < 85% or uncertain.
    """
    return get_pending_verifications()

@router.get("/records/{record_id}")
def get_record(record_id: str):
    rec = get_record_by_id(record_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Land record not found")
    
    # Also fetch linked disputes
    all_disputes = get_all_disputes()
    linked_disputes = [d for d in all_disputes if record_id in d.get("record_ids", [])]
    return {
        "record": rec,
        "disputes": linked_disputes
    }

@router.get("/records/{record_id}/document-svg")
def get_document_svg(record_id: str):
    """
    Generates and returns an SVG digital facsimile of the original revenue register / deed
    for visual side-by-side human officer inspection.
    """
    rec = get_record_by_id(record_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Land record not found")
    svg_content = generate_document_svg(rec)
    return Response(content=svg_content, media_type="image/svg+xml")

@router.post("/records/{record_id}/verify")
def human_verify_record(
    record_id: str,
    payload: Dict[str, Any] = Body(...)
):
    """
    Human-in-the-Loop Verification Action:
    Revenue Officer / Patwari reviews uncertain or faded fields, modifies or certifies values,
    and approves the record into the permanent ledger.
    """
    rec = get_record_by_id(record_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Land record not found")

    officer_name = payload.get("officer_name", "Tehsildar / Revenue Officer Sadar")
    remarks = payload.get("remarks", "Verified against physical revenue register.")
    corrected_fields = payload.get("corrected_fields", {})
    now = datetime.now(timezone.utc).isoformat()

    # Track correction history for AI continuous learning feedback loop
    corrections_logged = []
    for field_name, new_val in corrected_fields.items():
        old_val = rec.get(field_name)
        if str(old_val) != str(new_val):
            corrections_logged.append({
                "field": field_name,
                "old_value": old_val,
                "corrected_value": new_val,
                "verified_by": officer_name,
                "timestamp": now
            })
            rec[field_name] = new_val

            # Reset field confidence to 100% since human certified
            if "field_confidences" in rec and field_name in rec["field_confidences"]:
                rec["field_confidences"][field_name]["confidence"] = 1.0
                rec["field_confidences"][field_name]["is_low_confidence"] = False
                rec["field_confidences"][field_name]["value"] = new_val

    # Recalculate metrics
    if "area_sq_meters" in rec:
        rec["area_hectares"] = round(float(rec["area_sq_meters"]) / 10000.0, 4)
        rec["area_acres"] = round(float(rec["area_sq_meters"]) / 4046.86, 4)

    # Re-run validation with updated fields
    existing_records = get_all_records()
    dispute_status, dispute_tags, created_disputes, conf, _ = validate_land_record(rec, existing_records)
    
    rec["dispute_status"] = dispute_status
    rec["dispute_tags"] = dispute_tags
    rec["confidence_score"] = 1.0  # Certified by officer
    rec["verification_status"] = VerificationStatus.VERIFIED_BY_OFFICER.value
    rec["verified_by"] = officer_name
    rec["verified_at"] = now
    rec["updated_at"] = now
    
    existing_history = rec.get("correction_history", [])
    if corrections_logged:
        existing_history.extend(corrections_logged)
    rec["correction_history"] = existing_history
    rec["audit_hash"] = calculate_sha256(rec)

    save_record(rec)

    # Immutable Blockchain Audit Event
    block_hash = record_audit_event(
        action="HUMAN_VERIFICATION_APPROVED",
        record_id=record_id,
        details=f"Record verified by Officer {officer_name}: {remarks}. {len(corrections_logged)} fields corrected.",
        payload={"corrections": corrections_logged, "remarks": remarks, "officer": officer_name}
    )

    return {
        "success": True,
        "message": f"Land Record {record_id} successfully verified and certified by {officer_name}.",
        "record": rec,
        "audit_hash": block_hash
    }

@router.post("/records/digitize")
def digitize_record(payload: Dict[str, Any] = Body(...)):
    """
    Accepts raw OCR text OR structured record data.
    Runs automated multilingual extraction, validation & spatial conflict checks.
    Stores record, logs to blockchain audit ledger.
    """
    now = datetime.now(timezone.utc).isoformat()
    
    # 1. OCR text extraction if raw text is passed
    if "raw_text" in payload and not payload.get("khasra_no"):
        extracted = extract_land_record_from_text(payload["raw_text"])
        data = {**extracted, **payload}
    else:
        data = payload

    khasra_no = data.get("khasra_no", "").strip()
    if not khasra_no:
        raise HTTPException(status_code=400, detail="Khasra/Survey Number is required")

    area_sqm = float(data.get("area_sq_meters", 2000.0))
    area_hectares = round(area_sqm / 10000.0, 4)
    area_acres = round(area_sqm / 4046.86, 4)

    record_id = data.get("id") or f"REC-{uuid.uuid4().hex[:8].upper()}"

    record_candidate = {
        "id": record_id,
        "khasra_no": khasra_no,
        "khata_no": data.get("khata_no", "1"),
        "village": data.get("village", "Rampur"),
        "tehsil": data.get("tehsil", "Sadar"),
        "district": data.get("district", "Varanasi"),
        "state": data.get("state", "Uttar Pradesh"),
        "area_sq_meters": area_sqm,
        "area_hectares": area_hectares,
        "area_acres": area_acres,
        "land_type": data.get("land_type", "Agricultural"),
        "language": data.get("language", "Hindi (हिंदी)"),
        "document_type": data.get("document_type", "Scanned PDF / Khasra"),
        "mutation_no": data.get("mutation_no"),
        "registration_date": data.get("registration_date", now[:10]),
        "owners": data.get("owners", [{"name": "Registered Owner", "aadhaar_masked": "XXXX-XXXX-1111", "share_percentage": 100.0}]),
        "boundary_geojson": data.get("boundary_geojson") or {
            "type": "Polygon",
            "coordinates": [[[82.980, 25.310], [82.982, 25.310], [82.982, 25.308], [82.980, 25.308], [82.980, 25.310]]]
        },
        "field_confidences": data.get("field_confidences", {}),
        "document_source": data.get("document_source", "Scanned Revenue Deed"),
        "dilrmp_cross_verified": data.get("dilrmp_cross_verified", True),
        "correction_history": [],
        "created_at": now,
        "updated_at": now
    }

    # 2. Run Intelligent Validation & Spatial Conflict Check
    existing_records = get_all_records()
    dispute_status, dispute_tags, created_disputes, conf, verification_status = validate_land_record(record_candidate, existing_records)

    record_candidate["dispute_status"] = dispute_status
    record_candidate["dispute_tags"] = dispute_tags
    record_candidate["confidence_score"] = conf
    record_candidate["verification_status"] = verification_status
    record_candidate["audit_hash"] = calculate_sha256(record_candidate)

    # 3. Save Record & Disputes
    save_record(record_candidate)
    for d in created_disputes:
        save_dispute(d)
        record_audit_event(
            action="DISPUTE_FLAGGED",
            record_id=d["id"],
            details=f"Dispute flagged for Khasra #{khasra_no}: {d['title']}",
            payload=d
        )

    # 4. Immutable Blockchain Audit Entry
    block_hash = record_audit_event(
        action="DIGITIZE_RECORD",
        record_id=record_id,
        details=f"Digitized Khasra #{khasra_no} ({record_candidate['village']}, {record_candidate['state']}) with status {dispute_status} ({verification_status})",
        payload=record_candidate
    )

    return {
        "success": True,
        "record": record_candidate,
        "disputes_detected": created_disputes,
        "verification_status": verification_status,
        "audit_hash": block_hash
    }

@router.get("/disputes/")
def list_disputes(status: Optional[str] = None):
    return get_all_disputes(status=status)

@router.post("/disputes/{dispute_id}/resolve")
def resolve_dispute(
    dispute_id: str,
    payload: Dict[str, Any] = Body(...)
):
    """
    Revenue Officer resolution action: approves or clarifies boundary disputes.
    Logs mutation to cryptographic audit ledger.
    """
    all_disputes = get_all_disputes()
    dispute = next((d for d in all_disputes if d["id"] == dispute_id), None)
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")

    action = payload.get("action", "RESOLVED")  # RESOLVED or DISMISSED
    notes = payload.get("resolution_notes", "Resolved after field demarcation & Patwari survey.")
    now = datetime.now(timezone.utc).isoformat()

    update_dispute_status(dispute_id, action, notes, now)

    # Update status of linked records if no other active disputes exist
    record_ids = dispute.get("record_ids", [])
    remaining_disputes = [d for d in all_disputes if d["id"] != dispute_id and d["status"] == "ACTIVE"]

    for rid in record_ids:
        rec = get_record_by_id(rid)
        if rec:
            has_other_active = any(rid in d.get("record_ids", []) for d in remaining_disputes)
            if not has_other_active:
                rec["dispute_status"] = DisputeStatus.RESOLVED.value
                rec["updated_at"] = now
                rec["audit_hash"] = calculate_sha256(rec)
                save_record(rec)

    # Log to audit ledger
    record_audit_event(
        action="RESOLVE_DISPUTE",
        record_id=dispute_id,
        details=f"Dispute {dispute_id} resolved by Revenue Officer: {notes}",
        payload={"dispute_id": dispute_id, "action": action, "notes": notes, "timestamp": now}
    )

    return {"success": True, "message": f"Dispute {dispute_id} has been marked as {action}."}

@router.get("/gis/parcels")
def get_gis_geojson():
    """
    Returns a GeoJSON FeatureCollection of all cadastral parcels + overlap dispute polygons.
    Formatted for Leaflet.js rendering.
    """
    records = get_all_records()
    disputes = get_all_disputes(status="ACTIVE")

    features = []

    # Parcel polygons
    for r in records:
        features.append({
            "type": "Feature",
            "id": r["id"],
            "geometry": r["boundary_geojson"],
            "properties": {
                "id": r["id"],
                "khasra_no": r["khasra_no"],
                "khata_no": r["khata_no"],
                "village": r["village"],
                "area_sq_meters": r["area_sq_meters"],
                "land_type": r["land_type"],
                "dispute_status": r["dispute_status"],
                "verification_status": r.get("verification_status", "AUTO_VERIFIED"),
                "owners": r["owners"],
                "confidence_score": r["confidence_score"],
                "feature_type": "PARCEL"
            }
        })

    # Active Overlap polygons (encroachments)
    for d in disputes:
        if d.get("overlap_geojson"):
            features.append({
                "type": "Feature",
                "id": d["id"],
                "geometry": d["overlap_geojson"],
                "properties": {
                    "id": d["id"],
                    "title": d["title"],
                    "description": d["description"],
                    "dispute_type": d["dispute_type"],
                    "severity": d["severity"],
                    "overlap_area_sq_meters": d.get("overlap_area_sq_meters"),
                    "record_ids": d["record_ids"],
                    "feature_type": "DISPUTE_OVERLAP"
                }
            })

    return {
        "type": "FeatureCollection",
        "features": features
    }

@router.get("/integrations/dilrmp-check")
def check_dilrmp(state: str = "Uttar Pradesh", district: str = "Varanasi", survey_no: str = "105"):
    """
    Mock DILRMP National Land Records Modernization API check.
    Cross-checks ownership and encumbrance certificate across central registries.
    """
    return {
        "status": "SUCCESS",
        "portal": "DILRMP-National-Gateway",
        "state_registry": f"Bhulekh-{state.replace(' ', '')}",
        "district": district,
        "survey_number": survey_no,
        "cross_check_status": "MATCH_FOUND",
        "aadhaar_vault_masked": True,
        "encumbrance_status": "FREE",
        "last_sync": datetime.now(timezone.utc).isoformat()
    }

@router.get("/audit/ledger")
def get_ledger():
    return get_audit_ledger()

@router.get("/audit/verify")
def verify_ledger():
    is_valid, blocks, message = verify_audit_ledger()
    return {
        "is_valid": is_valid,
        "total_blocks": len(blocks),
        "status_message": message
    }
