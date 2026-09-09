import uuid
from datetime import datetime, timezone
from backend.database import init_db, save_record, save_dispute, get_all_records, get_record_by_id
from backend.models import LandClassification, DisputeStatus, DisputeType, VerificationStatus
from backend.validation_engine import validate_land_record
from backend.blockchain_audit import record_audit_event, calculate_sha256

def seed_database(force=False):
    init_db()
    
    # Check if records already exist
    existing = get_all_records()
    if len(existing) >= 6 and not force:
        print(f"Database already contains {len(existing)} records. Skipping seed.")
        return

    if force:
        from backend.database import get_db_connection
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM records")
        c.execute("DELETE FROM disputes")
        c.execute("DELETE FROM audit_ledger")
        conn.commit()
        conn.close()
        print("Existing database cleared for fresh seeding.")

    print("Seeding database with cadastral parcels across Uttar Pradesh, Maharashtra, and Telangana...")

    now = datetime.now(timezone.utc).isoformat()

    # 1. Parcel 101 - Clear agricultural parcel (UP)
    p101_boundary = {
        "type": "Polygon",
        "coordinates": [[[82.9770, 25.3130], [82.9790, 25.3130], [82.9790, 25.3115], [82.9770, 25.3115], [82.9770, 25.3130]]]
    }
    p101 = {
        "id": "REC-RAMPUR-101",
        "khasra_no": "101",
        "khata_no": "45",
        "village": "Rampur",
        "tehsil": "Sadar",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "area_sq_meters": 3200.0,
        "area_hectares": 0.32,
        "area_acres": 0.79,
        "land_type": LandClassification.AGRICULTURAL.value,
        "language": "Hindi (हिंदी)",
        "document_type": "Scanned PDF / Khasra",
        "verification_status": VerificationStatus.AUTO_VERIFIED.value,
        "owners": [
            {"name": "Rajesh Verma", "aadhaar_masked": "XXXX-XXXX-8812", "share_percentage": 100.0, "father_or_husband_name": "Ram Lakhan Verma", "confidence": 0.99}
        ],
        "boundary_geojson": p101_boundary,
        "field_confidences": {
            "khasra_no": {"value": "101", "confidence": 0.99, "is_low_confidence": False},
            "khata_no": {"value": "45", "confidence": 0.98, "is_low_confidence": False},
            "area_sq_meters": {"value": 3200.0, "confidence": 0.98, "is_low_confidence": False},
            "owners": {"value": "Rajesh Verma", "confidence": 0.99, "is_low_confidence": False}
        },
        "dispute_status": DisputeStatus.CLEAR.value,
        "dispute_tags": [],
        "confidence_score": 0.99,
        "document_source": "UP Bhulekh Digital Khatauni 2024",
        "dilrmp_cross_verified": True,
        "audit_hash": "",
        "created_at": now,
        "updated_at": now
    }
    p101["audit_hash"] = calculate_sha256(p101)
    save_record(p101)
    record_audit_event("DIGITIZE_RECORD", p101["id"], "Khasra #101 digitized and verified from UP Bhulekh portal", p101)

    # 2. Parcel 102 - Encroaching parcel (overlaps with eastern border of 101)
    p102_boundary = {
        "type": "Polygon",
        "coordinates": [[[82.9785, 25.3125], [82.9805, 25.3125], [82.9805, 25.3105], [82.9785, 25.3105], [82.9785, 25.3125]]]
    }
    p102_data = {
        "id": "REC-RAMPUR-102",
        "khasra_no": "102",
        "khata_no": "52",
        "village": "Rampur",
        "tehsil": "Sadar",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "area_sq_meters": 2900.0,
        "area_hectares": 0.29,
        "area_acres": 0.72,
        "land_type": LandClassification.AGRICULTURAL.value,
        "language": "Hindi (हिंदी)",
        "document_type": "Scanned PDF / Khasra",
        "verification_status": VerificationStatus.AUTO_VERIFIED.value,
        "owners": [
            {"name": "Dhirendra Nath Mishra", "aadhaar_masked": "XXXX-XXXX-3341", "share_percentage": 100.0, "father_or_husband_name": "B.N. Mishra", "confidence": 0.95}
        ],
        "boundary_geojson": p102_boundary,
        "field_confidences": {
            "khasra_no": {"value": "102", "confidence": 0.96, "is_low_confidence": False},
            "khata_no": {"value": "52", "confidence": 0.95, "is_low_confidence": False},
            "area_sq_meters": {"value": 2900.0, "confidence": 0.94, "is_low_confidence": False}
        },
        "document_source": "Legacy Paper Registry Deed (Unverified)",
        "dilrmp_cross_verified": False,
        "created_at": now,
        "updated_at": now
    }
    status, tags, disputes, conf, ver_status = validate_land_record(p102_data, [p101])
    p102 = {
        **p102_data,
        "dispute_status": status,
        "dispute_tags": tags,
        "confidence_score": conf,
        "verification_status": ver_status,
        "audit_hash": ""
    }
    p102["audit_hash"] = calculate_sha256(p102)
    save_record(p102)
    for d in disputes:
        save_dispute(d)
        record_audit_event("DISPUTE_FLAGGED", d["id"], "Critical spatial boundary overlap flagged between Khasra 101 and 102", d)
    record_audit_event("DIGITIZE_RECORD", p102["id"], "Khasra #102 ingested; flagged for boundary encroachment review", p102)

    # 3. Parcel 103 - Commercial parcel
    p103_boundary = {
        "type": "Polygon",
        "coordinates": [[[82.9810, 25.3130], [82.9830, 25.3130], [82.9830, 25.3115], [82.9810, 25.3115], [82.9810, 25.3130]]]
    }
    p103 = {
        "id": "REC-RAMPUR-103",
        "khasra_no": "103",
        "khata_no": "89",
        "village": "Rampur",
        "tehsil": "Sadar",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "area_sq_meters": 3100.0,
        "area_hectares": 0.31,
        "area_acres": 0.77,
        "land_type": LandClassification.COMMERCIAL.value,
        "language": "Hindi (हिंदी)",
        "document_type": "Scanned PDF / Khasra",
        "verification_status": VerificationStatus.AUTO_VERIFIED.value,
        "owners": [
            {"name": "Amit Sharma", "aadhaar_masked": "XXXX-XXXX-9102", "share_percentage": 50.0, "father_or_husband_name": "Satish Sharma", "confidence": 0.98},
            {"name": "Priya Sharma", "aadhaar_masked": "XXXX-XXXX-9103", "share_percentage": 50.0, "father_or_husband_name": "Amit Sharma", "confidence": 0.98}
        ],
        "boundary_geojson": p103_boundary,
        "field_confidences": {
            "khasra_no": {"value": "103", "confidence": 0.98, "is_low_confidence": False},
            "khata_no": {"value": "89", "confidence": 0.97, "is_low_confidence": False},
            "area_sq_meters": {"value": 3100.0, "confidence": 0.98, "is_low_confidence": False}
        },
        "dispute_status": DisputeStatus.CLEAR.value,
        "dispute_tags": [],
        "confidence_score": 0.98,
        "document_source": "Commercial Mutation Sanction Order 2025",
        "dilrmp_cross_verified": True,
        "audit_hash": "",
        "created_at": now,
        "updated_at": now
    }
    p103["audit_hash"] = calculate_sha256(p103)
    save_record(p103)
    record_audit_event("DIGITIZE_RECORD", p103["id"], "Khasra #103 commercial parcel digitized with verified 50/50 spousal share", p103)

    # 4. Parcel 104 - Residential parcel
    p104_boundary = {
        "type": "Polygon",
        "coordinates": [[[82.9835, 25.3130], [82.9855, 25.3130], [82.9855, 25.3115], [82.9835, 25.3115], [82.9835, 25.3130]]]
    }
    p104 = {
        "id": "REC-RAMPUR-104",
        "khasra_no": "104",
        "khata_no": "94",
        "village": "Rampur",
        "tehsil": "Sadar",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "area_sq_meters": 2800.0,
        "area_hectares": 0.28,
        "area_acres": 0.69,
        "land_type": LandClassification.RESIDENTIAL.value,
        "language": "English",
        "document_type": "Scanned PDF / Khasra",
        "verification_status": VerificationStatus.AUTO_VERIFIED.value,
        "owners": [
            {"name": "Vikram Patel", "aadhaar_masked": "XXXX-XXXX-1990", "share_percentage": 100.0, "father_or_husband_name": "D.K. Patel", "confidence": 0.97}
        ],
        "boundary_geojson": p104_boundary,
        "field_confidences": {
            "khasra_no": {"value": "104", "confidence": 0.97, "is_low_confidence": False},
            "khata_no": {"value": "94", "confidence": 0.97, "is_low_confidence": False}
        },
        "dispute_status": DisputeStatus.CLEAR.value,
        "dispute_tags": [],
        "confidence_score": 0.97,
        "document_source": "Gram Panchayat Housing Registry",
        "dilrmp_cross_verified": True,
        "audit_hash": "",
        "created_at": now,
        "updated_at": now
    }
    p104["audit_hash"] = calculate_sha256(p104)
    save_record(p104)
    record_audit_event("DIGITIZE_RECORD", p104["id"], "Khasra #104 residential plot registered", p104)

    # 5. Parcel 115 - Faded Handwritten Register needing Human Verification (UP)
    p115_boundary = {
        "type": "Polygon",
        "coordinates": [[[82.9870, 25.3090], [82.9890, 25.3090], [82.9890, 25.3075], [82.9870, 25.3075], [82.9870, 25.3090]]]
    }
    p115 = {
        "id": "REC-RAMPUR-115-PENDING",
        "khasra_no": "115",
        "khata_no": "63",
        "village": "Rampur",
        "tehsil": "Sadar",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "area_sq_meters": 1600.0,
        "area_hectares": 0.16,
        "area_acres": 0.395,
        "land_type": LandClassification.AGRICULTURAL.value,
        "language": "Hindi (हिंदी)",
        "document_type": "Handwritten Register",
        "verification_status": VerificationStatus.PENDING_VERIFICATION.value,
        "owners": [
            {"name": "Jagannath Ram", "aadhaar_masked": "XXXX-XXXX-8812", "share_percentage": 100.0, "father_or_husband_name": "Kashi Ram", "confidence": 0.62}
        ],
        "boundary_geojson": p115_boundary,
        "field_confidences": {
            "khasra_no": {"value": "115", "confidence": 0.72, "is_low_confidence": True},
            "khata_no": {"value": "63", "confidence": 0.88, "is_low_confidence": False},
            "area_sq_meters": {"value": 1600.0, "confidence": 0.68, "is_low_confidence": True},
            "owners": {"value": "Jagannath Ram", "confidence": 0.62, "is_low_confidence": True}
        },
        "dispute_status": DisputeStatus.WARNING.value,
        "dispute_tags": ["Uncertain OCR: Faded handwriting (<85% confidence)", "Pending Patwari / Officer Physical Register Verification"],
        "confidence_score": 0.71,
        "document_source": "Historical Handwritten Settlement Register 1988 (Faded)",
        "dilrmp_cross_verified": False,
        "audit_hash": "",
        "created_at": now,
        "updated_at": now
    }
    p115["audit_hash"] = calculate_sha256(p115)
    save_record(p115)
    record_audit_event("DIGITIZE_RECORD", p115["id"], "Khasra #115 digitized with low confidence (71%); queued for Human Officer Verification", p115)

    # 6. Maharashtra Satbara (7/12) - Pune/Haveli Gat 142/A (Maharashtra)
    p_mh_boundary = {
        "type": "Polygon",
        "coordinates": [[[73.8500, 18.5200], [73.8525, 18.5200], [73.8525, 18.5180], [73.8500, 18.5180], [73.8500, 18.5200]]]
    }
    p_mh = {
        "id": "REC-MAHA-PUNE-142A",
        "khasra_no": "142/A",
        "khata_no": "215",
        "village": "Theur",
        "tehsil": "Haveli",
        "district": "Pune",
        "state": "Maharashtra",
        "area_sq_meters": 3200.0,
        "area_hectares": 0.32,
        "area_acres": 0.79,
        "land_type": LandClassification.AGRICULTURAL.value,
        "language": "Marathi (मराठी)",
        "document_type": "Scanned PDF / Khasra",
        "verification_status": VerificationStatus.AUTO_VERIFIED.value,
        "mutation_no": "M-2024/8912",
        "owners": [
            {"name": "Balasaheb Tukaram Patil", "aadhaar_masked": "XXXX-XXXX-6612", "share_percentage": 100.0, "father_or_husband_name": "Tukaram Patil", "confidence": 0.98}
        ],
        "boundary_geojson": p_mh_boundary,
        "field_confidences": {
            "khasra_no": {"value": "142/A", "confidence": 0.99, "is_low_confidence": False},
            "khata_no": {"value": "215", "confidence": 0.98, "is_low_confidence": False},
            "area_sq_meters": {"value": 3200.0, "confidence": 0.96, "is_low_confidence": False}
        },
        "dispute_status": DisputeStatus.CLEAR.value,
        "dispute_tags": [],
        "confidence_score": 0.98,
        "document_source": "Maharashtra Mahabhulekh 7/12 Digital Extract",
        "dilrmp_cross_verified": True,
        "audit_hash": "",
        "created_at": now,
        "updated_at": now
    }
    p_mh["audit_hash"] = calculate_sha256(p_mh)
    save_record(p_mh)
    record_audit_event("DIGITIZE_RECORD", p_mh["id"], "Maharashtra Pune Haveli Gat 142/A Satbara digitized and certified", p_mh)

    # 7. Telangana Dharani Pahani - Survey 88/2 (Telangana)
    p_ts_boundary = {
        "type": "Polygon",
        "coordinates": [[[78.3550, 17.4620], [78.3580, 17.4620], [78.3580, 17.4595], [78.3550, 17.4595], [78.3550, 17.4620]]]
    }
    p_ts = {
        "id": "REC-TS-RR-88",
        "khasra_no": "88/2",
        "khata_no": "310",
        "village": "Kondapur",
        "tehsil": "Serilingampally",
        "district": "Ranga Reddy",
        "state": "Telangana",
        "area_sq_meters": 4500.0,
        "area_hectares": 0.45,
        "area_acres": 1.112,
        "land_type": LandClassification.AGRICULTURAL.value,
        "language": "Telugu (తెలుగు)",
        "document_type": "Scanned PDF / Khasra",
        "verification_status": VerificationStatus.AUTO_VERIFIED.value,
        "owners": [
            {"name": "Katam Venkat Rao", "aadhaar_masked": "XXXX-XXXX-2109", "share_percentage": 100.0, "father_or_husband_name": "Narayana Rao", "confidence": 0.97}
        ],
        "boundary_geojson": p_ts_boundary,
        "field_confidences": {
            "khasra_no": {"value": "88/2", "confidence": 0.98, "is_low_confidence": False},
            "khata_no": {"value": "310", "confidence": 0.97, "is_low_confidence": False},
            "area_sq_meters": {"value": 4500.0, "confidence": 0.95, "is_low_confidence": False}
        },
        "dispute_status": DisputeStatus.CLEAR.value,
        "dispute_tags": [],
        "confidence_score": 0.97,
        "document_source": "Telangana Dharani Integrated Land Records Portal",
        "dilrmp_cross_verified": True,
        "audit_hash": "",
        "created_at": now,
        "updated_at": now
    }
    p_ts["audit_hash"] = calculate_sha256(p_ts)
    save_record(p_ts)
    record_audit_event("DIGITIZE_RECORD", p_ts["id"], "Telangana Survey 88/2 Pahani/Adangal digitized into central repository", p_ts)

    print(f"Seed complete! Initialized 7 multi-state cadastral parcels and 1 boundary dispute.")

if __name__ == "__main__":
    seed_database()
