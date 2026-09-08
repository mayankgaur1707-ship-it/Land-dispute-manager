import uuid
from datetime import datetime, timezone
from backend.database import init_db, save_record, save_dispute, get_all_records
from backend.models import LandClassification, DisputeStatus, DisputeType
from backend.validation_engine import validate_land_record
from backend.blockchain_audit import record_audit_event, calculate_sha256

def seed_database():
    init_db()
    
    # Check if records already exist
    existing = get_all_records()
    if existing:
        print(f"Database already contains {len(existing)} records. Skipping seed.")
        return

    print("Seeding database with cadastral parcels in Rampur Village...")

    now = datetime.now(timezone.utc).isoformat()

    # 1. Parcel 101 - Clear agricultural parcel
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
        "owners": [
            {"name": "Rajesh Verma", "aadhaar_masked": "XXXX-XXXX-8812", "share_percentage": 100.0, "father_or_husband_name": "Ram Lakhan Verma"}
        ],
        "boundary_geojson": p101_boundary,
        "dispute_status": DisputeStatus.CLEAR.value,
        "dispute_tags": [],
        "confidence_score": 0.99,
        "document_source": "UP Bhulekh Digital Khatauni 2024",
        "audit_hash": "",
        "created_at": now,
        "updated_at": now
    }
    p101["audit_hash"] = calculate_sha256(p101)
    save_record(p101)
    record_audit_event("DIGITIZE_RECORD", p101["id"], "Khasra #101 digitized and verified from State Bhulekh portal", p101)

    # 2. Parcel 102 - Encroaching parcel (overlaps with eastern border of 101)
    # Notice: coordinates [82.9785, 25.3125] to [82.9805, 25.3125] intersects [82.9770-82.9790, 25.3115-25.3130]!
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
        "owners": [
            {"name": "Dhirendra Nath Mishra", "aadhaar_masked": "XXXX-XXXX-3341", "share_percentage": 100.0, "father_or_husband_name": "B.N. Mishra"}
        ],
        "boundary_geojson": p102_boundary,
        "document_source": "Legacy Paper Registry Deed (Unverified)",
        "created_at": now,
        "updated_at": now
    }
    # Validate against existing p101
    status, tags, disputes, conf = validate_land_record(p102_data, [p101])
    p102 = {
        **p102_data,
        "dispute_status": status,
        "dispute_tags": tags,
        "confidence_score": conf,
        "audit_hash": ""
    }
    p102["audit_hash"] = calculate_sha256(p102)
    save_record(p102)
    for d in disputes:
        save_dispute(d)
        record_audit_event("DISPUTE_FLAGGED", d["id"], f"Critical spatial boundary overlap flagged between Khasra 101 and 102", d)
    record_audit_event("DIGITIZE_RECORD", p102["id"], "Khasra #102 ingested; flagged for boundary encroachment review", p102)

    # 3. Parcel 103 - Commercial plot on highway
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
        "owners": [
            {"name": "Amit Sharma", "aadhaar_masked": "XXXX-XXXX-9102", "share_percentage": 50.0, "father_or_husband_name": "Satish Sharma"},
            {"name": "Priya Sharma", "aadhaar_masked": "XXXX-XXXX-9103", "share_percentage": 50.0, "father_or_husband_name": "Amit Sharma"}
        ],
        "boundary_geojson": p103_boundary,
        "dispute_status": DisputeStatus.CLEAR.value,
        "dispute_tags": [],
        "confidence_score": 0.98,
        "document_source": "Commercial Mutation Sanction Order 2025",
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
        "owners": [
            {"name": "Vikram Patel", "aadhaar_masked": "XXXX-XXXX-1990", "share_percentage": 100.0, "father_or_husband_name": "D.K. Patel"}
        ],
        "boundary_geojson": p104_boundary,
        "dispute_status": DisputeStatus.CLEAR.value,
        "dispute_tags": [],
        "confidence_score": 0.97,
        "document_source": "Gram Panchayat Housing Registry",
        "audit_hash": "",
        "created_at": now,
        "updated_at": now
    }
    p104["audit_hash"] = calculate_sha256(p104)
    save_record(p104)
    record_audit_event("DIGITIZE_RECORD", p104["id"], "Khasra #104 residential plot registered", p104)

    print("Seed complete! Initialized 4 cadastral parcels and 1 boundary dispute.")

if __name__ == "__main__":
    seed_database()
