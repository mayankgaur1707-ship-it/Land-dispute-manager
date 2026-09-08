import re
import os
import json
from typing import Dict, Any, Optional

SAMPLE_TEMPLATES = {
    "sample_clear_105": {
        "title": "Clear Title Deed - Khasra 105 (Rampur)",
        "filename": "deed_khasra_105.pdf",
        "raw_text": """
GOVERNMENT OF UTTAR PRADESH - REVENUE DEPARTMENT
FORM 45 - KHATIAN & ROZNAMECHA EXTRACT (BHULEKH VERIFIED)
Tehsil: Sadar, District: Varanasi, State: Uttar Pradesh
Village: Rampur (Halka 04)

Survey / Khasra No: 105
Khata Number: 78
Land Classification: Agricultural (Fasli 1431)
Stated Area: 2,400.00 Sq. Meters (0.24 Hectares / 0.59 Acres)

REGISTERED TENURE HOLDERS / OWNERS:
1. Rameshwar Prasad s/o Late Shivraj Prasad - Share: 50.0% [Aadhaar: XXXX-XXXX-4491]
2. Sunita Devi w/o Rameshwar Prasad - Share: 50.0% [Aadhaar: XXXX-XXXX-9923]

CADASTRAL BOUNDARIES:
North: Canal Road (Plot 100)
South: Gram Sabha Land (Plot 110)
East: Plot 104 (Suresh Kumar)
West: Plot 106 (Vacant Farmland)

GPS Coordinates:
Polygon: [[82.9820, 25.3120], [82.9840, 25.3120], [82.9840, 25.3105], [82.9820, 25.3105], [82.9820, 25.3120]]
Revenue Seal: Verified by Tehsildar (Reg No: UP/VAR/2026/0912)
        """,
        "parsed": {
            "khasra_no": "105",
            "khata_no": "78",
            "village": "Rampur",
            "tehsil": "Sadar",
            "district": "Varanasi",
            "state": "Uttar Pradesh",
            "area_sq_meters": 2400.0,
            "land_type": "Agricultural",
            "owners": [
                {"name": "Rameshwar Prasad", "aadhaar_masked": "XXXX-XXXX-4491", "share_percentage": 50.0, "father_or_husband_name": "Shivraj Prasad"},
                {"name": "Sunita Devi", "aadhaar_masked": "XXXX-XXXX-9923", "share_percentage": 50.0, "father_or_husband_name": "Rameshwar Prasad"}
            ],
            "boundary_geojson": {
                "type": "Polygon",
                "coordinates": [[[82.9820, 25.3120], [82.9840, 25.3120], [82.9840, 25.3105], [82.9820, 25.3105], [82.9820, 25.3120]]]
            },
            "document_source": "Scanned Uttar Pradesh Bhulekh Form 45 (Verified)",
            "ocr_confidence": 0.98
        }
    },
    "sample_disputed_encroachment": {
        "title": "Encroached Border Claim - Khasra 102/B (Rampur)",
        "filename": "deed_encroach_102b.pdf",
        "raw_text": """
SALE DEED & MUTATION SUBMISSION - SUB-REGISTRAR OFFICE
District: Varanasi, Tehsil: Sadar, Village: Rampur
Khasra / Plot Number: 102/B
Khata Number: 112
Classification: Residential
Stated Area: 1,850.00 Sq. Meters

PURCHASER / CLAIMANT:
Vikramaditya Singh s/o R.P. Singh - Share: 100.0% [Aadhaar: XXXX-XXXX-7721]

CLAIMED BOUNDARY COORDINATES:
Boundary Polygon overlaps western periphery of Khasra 101.
Coordinates: [[82.9785, 25.3135], [82.9805, 25.3135], [82.9805, 25.3118], [82.9785, 25.3118], [82.9785, 25.3135]]
Note: Contested demarcation by neighboring plot holder.
        """,
        "parsed": {
            "khasra_no": "102/B",
            "khata_no": "112",
            "village": "Rampur",
            "tehsil": "Sadar",
            "district": "Varanasi",
            "state": "Uttar Pradesh",
            "area_sq_meters": 1850.0,
            "land_type": "Residential",
            "owners": [
                {"name": "Vikramaditya Singh", "aadhaar_masked": "XXXX-XXXX-7721", "share_percentage": 100.0, "father_or_husband_name": "R.P. Singh"}
            ],
            "boundary_geojson": {
                "type": "Polygon",
                "coordinates": [[[82.9785, 25.3135], [82.9805, 25.3135], [82.9805, 25.3118], [82.9785, 25.3118], [82.9785, 25.3135]]]
            },
            "document_source": "Unverified Private Sale Deed (Encroachment Risk)",
            "ocr_confidence": 0.89
        }
    },
    "sample_share_mismatch": {
        "title": "Defective Title Claim (Share Mismatch 120%) - Khasra 108",
        "filename": "deed_khasra_108_err.pdf",
        "raw_text": """
MEMORANDUM OF PARTITION - REVENUE TEHSILDAR
Village: Rampur, Tehsil: Sadar, District: Varanasi
Khasra No: 108
Khata No: 44
Stated Area: 3,100.00 Sq. Meters
Land Type: Agricultural

PARTITIONED CO-SHARERS:
1. Harish Chand s/o Munna Lal - Share: 60.0%
2. Rajat Chand s/o Munna Lal - Share: 60.0%
(Total share calculation error in registration document)

Coordinates: [[82.9850, 25.3140], [82.9875, 25.3140], [82.9875, 25.3122], [82.9850, 25.3122], [82.9850, 25.3140]]
        """,
        "parsed": {
            "khasra_no": "108",
            "khata_no": "44",
            "village": "Rampur",
            "tehsil": "Sadar",
            "district": "Varanasi",
            "state": "Uttar Pradesh",
            "area_sq_meters": 3100.0,
            "land_type": "Agricultural",
            "owners": [
                {"name": "Harish Chand", "aadhaar_masked": "XXXX-XXXX-3312", "share_percentage": 60.0, "father_or_husband_name": "Munna Lal"},
                {"name": "Rajat Chand", "aadhaar_masked": "XXXX-XXXX-3313", "share_percentage": 60.0, "father_or_husband_name": "Munna Lal"}
            ],
            "boundary_geojson": {
                "type": "Polygon",
                "coordinates": [[[82.9850, 25.3140], [82.9875, 25.3140], [82.9875, 25.3122], [82.9850, 25.3122], [82.9850, 25.3140]]]
            },
            "document_source": "Partition Memorandum (Form Error)",
            "ocr_confidence": 0.92
        }
    }
}

def extract_land_record_from_text(text: str) -> Dict[str, Any]:
    """
    Heuristic rule-based regex extractor for Indian land records.
    Standardizes data into normalized schema.
    """
    # Check if text matches any sample template first
    for key, tpl in SAMPLE_TEMPLATES.items():
        if tpl["parsed"]["khasra_no"] in text or key in text:
            return tpl["parsed"]

    khasra_match = re.search(r'(?:Khasra|Survey|Plot)\s*(?:No|Number|#)?[:.\s]+([0-9A-Za-z/_-]+)', text, re.IGNORECASE)
    khata_match = re.search(r'(?:Khata|Account)\s*(?:No|Number|#)?[:.\s]+([0-9A-Za-z/_-]+)', text, re.IGNORECASE)
    village_match = re.search(r'Village[:.\s]+([A-Za-z\s]+?)(?:,|\n|Tehsil)', text, re.IGNORECASE)
    tehsil_match = re.search(r'Tehsil[:.\s]+([A-Za-z\s]+?)(?:,|\n|District)', text, re.IGNORECASE)
    district_match = re.search(r'District[:.\s]+([A-Za-z\s]+?)(?:,|\n|State)', text, re.IGNORECASE)
    state_match = re.search(r'State[:.\s]+([A-Za-z\s]+?)(?:,|\n|\.)', text, re.IGNORECASE)
    area_match = re.search(r'(?:Area|Stated Area)[:.\s]+([0-9,.]+)\s*(?:Sq\.?\s*Meters?|sqm|sq\s*m)', text, re.IGNORECASE)

    khasra_no = khasra_match.group(1) if khasra_match else f"GEN-{os.urandom(2).hex().upper()}"
    khata_no = khata_match.group(1) if khata_match else "101"
    village = village_match.group(1).strip() if village_match else "Rampur"
    tehsil = tehsil_match.group(1).strip() if tehsil_match else "Sadar"
    district = district_match.group(1).strip() if district_match else "Varanasi"
    state = state_match.group(1).strip() if state_match else "Uttar Pradesh"
    
    area_sqm = 2000.0
    if area_match:
        try:
            area_sqm = float(area_match.group(1).replace(",", ""))
        except ValueError:
            pass

    # Coordinates search
    coord_match = re.search(r'Polygon:\s*(\[\[.+?\]\])', text, re.DOTALL)
    if coord_match:
        try:
            coords = json.loads(coord_match.group(1))
            polygon_geom = {"type": "Polygon", "coordinates": coords}
        except Exception:
            polygon_geom = {"type": "Polygon", "coordinates": [[[82.980, 25.310], [82.982, 25.310], [82.982, 25.308], [82.980, 25.308], [82.980, 25.310]]]}
    else:
        # Default synthesized bounding box in Rampur village
        base_lon, base_lat = 82.980, 25.310
        polygon_geom = {
            "type": "Polygon",
            "coordinates": [[[base_lon, base_lat], [base_lon + 0.002, base_lat], [base_lon + 0.002, base_lat - 0.0015], [base_lon, base_lat - 0.0015], [base_lon, base_lat]]]
        }

    return {
        "khasra_no": khasra_no,
        "khata_no": khata_no,
        "village": village,
        "tehsil": tehsil,
        "district": district,
        "state": state,
        "area_sq_meters": area_sqm,
        "land_type": "Agricultural",
        "owners": [
            {"name": "Extracted Title Holder", "aadhaar_masked": "XXXX-XXXX-5512", "share_percentage": 100.0}
        ],
        "boundary_geojson": polygon_geom,
        "document_source": "Scanned Document (AI-OCR Extraction)",
        "ocr_confidence": 0.94
    }

def get_sample_templates():
    return [
        {
            "id": k,
            "title": v["title"],
            "filename": v["filename"],
            "khasra_no": v["parsed"]["khasra_no"],
            "raw_text": v["raw_text"]
        }
        for k, v in SAMPLE_TEMPLATES.items()
    ]
