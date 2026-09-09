import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Body, Depends, Header, File, UploadFile
from fastapi.responses import Response

from backend.models import (
    LandRecordCreate, LandRecord, DisputeRecord,
    DisputeStatus, DisputeType, VerificationStatus, HumanVerificationSubmission,
    UserSignUpRequest, UserSignInRequest, UserResponse, AuthTokenResponse
)
from backend.database import (
    get_all_records, get_record_by_id, save_record,
    get_all_disputes, save_dispute, update_dispute_status,
    get_audit_ledger, get_pending_verifications, get_state_district_analytics,
    create_user, get_user_by_email, get_user_by_id, update_user_last_login
)
from backend.validation_engine import validate_land_record
from backend.ocr_service import (
    extract_land_record_from_text, get_sample_templates, generate_document_svg,
    SAMPLE_TEMPLATES, scan_registry_document, generate_gemini_document_insights
)
from backend.blockchain_audit import record_audit_event, verify_audit_ledger, calculate_sha256
from backend.ai_assistant import process_chat_message
from backend.land_faq_kb import FAQ_CATEGORIES, POPULAR_FAQS, FAQS_BY_ID, search_faqs
from backend.auth import (
    hash_password, verify_password, create_access_token,
    validate_email_format, get_current_user_required, get_current_user_optional
)

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
    if "raw_text" in payload and payload.get("raw_text"):
        extracted = extract_land_record_from_text(payload["raw_text"])
        # Merge: extracted defaults overridden by non-empty user payload fields
        user_overrides = {k: v for k, v in payload.items() if v is not None and v != ""}
        data = {**extracted, **user_overrides}
    else:
        data = payload

    khasra_no = str(data.get("khasra_no", "")).strip()
    if not khasra_no:
        raise HTTPException(status_code=400, detail="Khasra/Survey Number is required")

    area_sqm = float(data.get("area_sq_meters", 2000.0))
    area_hectares = round(area_sqm / 10000.0, 4)
    area_acres = round(area_sqm / 4046.86, 4)

    record_id = data.get("id") or f"REC-{uuid.uuid4().hex[:8].upper()}"

    state_name = data.get("state", "Uttar Pradesh")
    if not data.get("boundary_geojson"):
        if "Maharashtra" in state_name:
            base_lon, base_lat = 73.850, 18.520
        elif "Telangana" in state_name:
            base_lon, base_lat = 78.355, 17.462
        else:
            base_lon, base_lat = 82.980, 25.310
        fallback_boundary = {
            "type": "Polygon",
            "coordinates": [[[base_lon, base_lat], [base_lon + 0.002, base_lat], [base_lon + 0.002, base_lat - 0.0015], [base_lon, base_lat - 0.0015], [base_lon, base_lat]]]
        }
    else:
        fallback_boundary = data.get("boundary_geojson")

    record_candidate = {
        "id": record_id,
        "khasra_no": khasra_no,
        "khata_no": str(data.get("khata_no", "1")),
        "village": data.get("village", "Rampur"),
        "tehsil": data.get("tehsil", "Sadar"),
        "district": data.get("district", "Varanasi"),
        "state": state_name,
        "area_sq_meters": area_sqm,
        "area_hectares": area_hectares,
        "area_acres": area_acres,
        "land_type": data.get("land_type", "Agricultural"),
        "language": data.get("language", "Hindi (हिंदी)"),
        "document_type": data.get("document_type", "Scanned PDF / Khasra"),
        "mutation_no": data.get("mutation_no"),
        "registration_date": data.get("registration_date", now[:10]),
        "owners": data.get("owners", [{"name": "Registered Owner", "aadhaar_masked": "XXXX-XXXX-1111", "share_percentage": 100.0}]),
        "boundary_geojson": fallback_boundary,
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

@router.post("/chat")
def chat_with_assistant(payload: Dict[str, Any] = Body(...)):
    """
    Bhoomi AI Sahayak (भूमि AI सहायक) Intelligent Land Assistant API:
    Answers questions about land disputes, specific cadastral parcels, legal remedies,
    mutation steps, bank loan title diligence, and generates actionable deep links.
    """
    message = payload.get("message", "").strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    role = payload.get("user_role", "REVENUE_OFFICER")
    api_key = payload.get("api_key")
    conversation_history = payload.get("conversation_history", [])
    current_record_id = payload.get("current_record_id")
    category_id = payload.get("category_id")
    state = payload.get("state")

    result = process_chat_message(
        message=message,
        role=role,
        api_key=api_key,
        conversation_history=conversation_history,
        current_record_id=current_record_id,
        state=state,
        category_id=category_id
    )
    return result

@router.get("/chat/suggestions")
def get_chat_suggestions(role: str = "REVENUE_OFFICER"):
    """
    Returns role-tailored prompt starters and popular legal / dispute questions.
    """
    common = [
        {"icon": "search", "label": "Status of Khasra 102", "query": "What is the status and dispute details for Khasra 102?"},
        {"icon": "scale", "label": "Resolve Boundary Overlap", "query": "How do I resolve a boundary encroachment under Section 24?"},
        {"icon": "file-text", "label": "Mutation (Dakhil Kharij)", "query": "What are the required documents and steps for land mutation?"},
        {"icon": "landmark", "label": "Bank Loan Eligibility", "query": "Is Khasra 101 eligible for a bank agricultural loan?"},
        {"icon": "shield-check", "label": "Verify Blockchain Ledger", "query": "How does the SHA-256 blockchain audit trail prevent land fraud?"}
    ]
    
    role_specific = {
        "CITIZEN_FARMER": [
            {"icon": "help-circle", "label": "मेरी जमीन पर विवाद है?", "query": "मेरी जमीन पर मेड़ का विवाद है, इसे कैसे सुलझाएं?"},
            {"icon": "file-check", "label": "दाखिल खारिज प्रक्रिया", "query": "दाखिल खारिज (Mutation) कराने में कितने दिन लगते हैं?"}
        ],
        "REVENUE_OFFICER": [
            {"icon": "map-pin", "label": "ETS Survey Procedure", "query": "What are the procedural steps for conducting an ETS field demarcation?"},
            {"icon": "check-square", "label": "Certify Pending Record", "query": "How do I review and certify low confidence OCR records in the queue?"}
        ],
        "BANK_OFFICER": [
            {"icon": "file-search", "label": "Form 15/16 Due Diligence", "query": "What checks are required for a 30-year non-encumbrance certificate?"},
            {"icon": "alert-circle", "label": "Assess Disputed Risk", "query": "Can a mortgage be created on a parcel flagged with WARNING status?"}
        ],
        "DILRMP_ADMIN": [
            {"icon": "bar-chart-2", "label": "State Progress Summary", "query": "Summarize the cadastral digitization rate across all pilot states."},
            {"icon": "cpu", "label": "OCR Continuous Learning", "query": "How does human officer feedback improve the ML OCR model accuracy?"}
        ]
    }
    
    specific = role_specific.get(role, role_specific["REVENUE_OFFICER"])
    return {
        "role": role,
        "suggestions": specific + common
    }

# -------------------------------------------------------------------------
# LAND RECORDS KNOWLEDGE BASE (184 FAQS) ENDPOINTS
# -------------------------------------------------------------------------

@router.get("/faq/categories")
def get_faq_categories():
    """
    Returns the list of 14 official Land Records FAQ categories with item counts.
    """
    return {"categories": FAQ_CATEGORIES}

@router.get("/faq/popular")
def get_popular_faqs():
    """
    Returns the top 18 citizen-popular Land Records questions.
    """
    popular = [FAQS_BY_ID[fid] for fid in POPULAR_FAQS if fid in FAQS_BY_ID]
    return {"popular_faqs": popular}

@router.get("/faq/search")
def search_faq_database(
    q: Optional[str] = None,
    category_id: Optional[str] = None,
    state: Optional[str] = None,
    limit: int = 50
):
    """
    Search and filter across the 184 Land Records FAQs by query, category, or state.
    """
    results = search_faqs(query=q, category_id=category_id, state=state, limit=limit)
    return {
        "count": len(results),
        "query": q,
        "category_id": category_id,
        "state": state,
        "results": results
    }

@router.get("/faq/{faq_id}")
def get_faq_by_id(faq_id: str):
    """
    Returns full details for a specific FAQ by ID.
    """
    if faq_id not in FAQS_BY_ID:
        raise HTTPException(status_code=404, detail=f"FAQ with ID '{faq_id}' not found")
    return FAQS_BY_ID[faq_id]

# -------------------------------------------------------------------------
# SECURITY & AUTHENTICATION ENDPOINTS (GMAIL & PASSWORD)
# -------------------------------------------------------------------------

@router.post("/auth/signup", response_model=AuthTokenResponse)
def sign_up(payload: UserSignUpRequest):
    """
    Registers a new user using a Gmail or official email address and password.
    Hashes password using PBKDF2-HMAC-SHA256 with 100,000 iterations.
    """
    clean_email = payload.email.strip().lower()
    
    if not validate_email_format(clean_email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email format. Please provide a valid email address (e.g., yourname@gmail.com)."
        )
    
    if len(payload.password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 6 characters long."
        )
        
    existing_user = get_user_by_email(clean_email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists. Please sign in instead."
        )
    
    user_id = f"USR-{uuid.uuid4().hex[:8].upper()}"
    pwd_hash, salt = hash_password(payload.password)
    now_iso = datetime.now(timezone.utc).isoformat()
    
    user_data = {
        "id": user_id,
        "email": clean_email,
        "full_name": payload.full_name.strip(),
        "password_hash": pwd_hash,
        "salt": salt,
        "role": payload.role.value if payload.role else "CITIZEN_FARMER",
        "phone": payload.phone.strip() if payload.phone else None,
        "created_at": now_iso,
        "last_login": now_iso,
        "is_active": True
    }
    
    saved_user = create_user(user_data)
    access_token = create_access_token(
        user_id=user_id,
        email=clean_email,
        role=saved_user["role"],
        expires_in_hours=72
    )
    
    user_resp = UserResponse(
        id=saved_user["id"],
        email=saved_user["email"],
        full_name=saved_user["full_name"],
        role=saved_user["role"],
        phone=saved_user.get("phone"),
        created_at=saved_user["created_at"],
        last_login=saved_user.get("last_login"),
        is_active=bool(saved_user.get("is_active", 1))
    )
    
    # Audit trail log for new user registration
    try:
        record_audit_event(
            action="USER_SIGNUP",
            record_id=user_id,
            details={
                "email": clean_email,
                "role": user_resp.role,
                "timestamp": now_iso
            }
        )
    except Exception:
        pass
    
    return AuthTokenResponse(access_token=access_token, user=user_resp)

@router.post("/auth/signin", response_model=AuthTokenResponse)
def sign_in(payload: UserSignInRequest):
    """
    Authenticates a user with Gmail/email and password using constant-time verification.
    """
    clean_email = payload.email.strip().lower()
    user = get_user_by_email(clean_email)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password. Please verify your credentials."
        )
        
    if not user.get("is_active", 1):
        raise HTTPException(
            status_code=403,
            detail="This account has been deactivated. Please contact DILRMP system administrator."
        )
        
    is_valid = verify_password(payload.password, user["salt"], user["password_hash"])
    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password. Please verify your credentials."
        )
        
    update_user_last_login(user["id"])
    now_iso = datetime.now(timezone.utc).isoformat()
    
    access_token = create_access_token(
        user_id=user["id"],
        email=clean_email,
        role=user["role"],
        expires_in_hours=72
    )
    
    user_resp = UserResponse(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        role=user["role"],
        phone=user.get("phone"),
        created_at=user["created_at"],
        last_login=now_iso,
        is_active=bool(user.get("is_active", 1))
    )
    
    return AuthTokenResponse(access_token=access_token, user=user_resp)

@router.get("/auth/me", response_model=UserResponse)
def get_current_user_profile(current_user: Dict[str, Any] = Depends(get_current_user_required)):
    """
    Returns the authenticated user's profile based on the Bearer token.
    """
    user = get_user_by_id(current_user.get("sub", ""))
    if not user:
        raise HTTPException(status_code=404, detail="User account not found or has been removed.")
    return UserResponse(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        role=user["role"],
        phone=user.get("phone"),
        created_at=user["created_at"],
        last_login=user.get("last_login"),
        is_active=bool(user.get("is_active", 1))
    )

@router.post("/auth/signout")
def sign_out():
    """
    Terminates client session.
    """
    return {"status": "success", "message": "Successfully signed out of BHOOMI system."}

# -------------------------------------------------------------------------
# AI REGISTRY DOCUMENT SCANNER & ACCURACY INSPECTION ENDPOINTS
# -------------------------------------------------------------------------

@router.post("/documents/scan")
async def scan_document_endpoint(
    file: Optional[UploadFile] = File(None),
    payload: Optional[Dict[str, Any]] = Body(None)
):
    """
    Scans an uploaded PDF or picture of a registry deed / Khasra document.
    Extracts owner names, registry/Khasra IDs, land details, computes accuracy,
    and returns both the saved record and corner HUD inspection metrics.
    """
    filename = "uploaded_registry_document.pdf"
    content_type = "application/pdf"
    file_bytes = None
    raw_text = None

    if file:
        filename = file.filename or "uploaded_registry_document.pdf"
        content_type = file.content_type or "application/pdf"
        file_bytes = await file.read()
    elif payload:
        filename = payload.get("filename", "sample_registry_deed.pdf")
        content_type = payload.get("content_type", "application/pdf")
        raw_text = payload.get("raw_text")
        if payload.get("sample_id"):
            sample_id = payload["sample_id"]
            if sample_id in SAMPLE_TEMPLATES:
                tmpl = SAMPLE_TEMPLATES[sample_id]
                filename = tmpl["filename"]
                raw_text = tmpl["raw_text"]

    scan_result = scan_registry_document(
        file_bytes=file_bytes,
        filename=filename,
        content_type=content_type,
        raw_text=raw_text
    )

    record = scan_result["scanned_record"]
    corner_hud = scan_result["corner_hud_data"]

    # Validate against existing records for spatial conflicts
    existing_records = get_all_records()
    dispute_status, dispute_tags, created_disputes, conf, verification_status = validate_land_record(record, existing_records)
    
    record["dispute_status"] = dispute_status
    record["dispute_tags"] = dispute_tags
    record["verification_status"] = verification_status
    record["audit_hash"] = calculate_sha256(record)

    # Persist in Database
    save_record(record)
    for d in created_disputes:
        save_dispute(d)

    # Log to Blockchain Audit Ledger
    block_hash = record_audit_event(
        action="DOCUMENT_AI_SCANNED",
        record_id=record["id"],
        details=f"AI scanned {filename}: Extracted {len(record['owners'])} owner(s), Khasra {record['khasra_no']}, Accuracy {scan_result['overall_accuracy']}%.",
        payload={
            "filename": filename,
            "overall_accuracy": scan_result["overall_accuracy"],
            "khasra_no": record["khasra_no"],
            "dispute_status": dispute_status
        }
    )

    return {
        "success": True,
        "message": f"Document '{filename}' scanned with {scan_result['overall_accuracy']}% accuracy and added to registry table.",
        "record": record,
        "corner_hud_data": corner_hud,
        "gemini_insights": corner_hud.get("gemini_insights"),
        "accuracy_report": {
            "overall_accuracy": scan_result["overall_accuracy"],
            "rating": corner_hud["accuracy_label"],
            "field_accuracies": corner_hud["field_accuracies"]
        },
        "audit_hash": block_hash
    }

@router.get("/documents/scanned")
def get_scanned_documents():
    """
    Returns all digitized/scanned land registry records for the table.
    """
    records = get_all_records()
    # Sort with newest first
    records_sorted = sorted(records, key=lambda r: r.get("created_at", ""), reverse=True)
    return {
        "count": len(records_sorted),
        "records": records_sorted
    }

@router.post("/ai/analyze-parcel")
def analyze_parcel_with_gemini(payload: Dict[str, Any] = Body(...)):
    """
    Real-time legal and cadastral risk analysis for any land record or parcel using Gemini 3.6 Flash.
    Provides instant risk score, title strength verdict, statutory references, and actionable next steps.
    """
    record_id = payload.get("record_id")
    khasra_no = payload.get("khasra_no")
    village = payload.get("village")
    
    target_record = None
    if record_id:
        target_record = get_record(record_id)
    elif khasra_no:
        records = get_all_records()
        for r in records:
            if str(r.get("khasra_no", "")).strip() == str(khasra_no).strip():
                if not village or str(r.get("village", "")).lower() == str(village).lower():
                    target_record = r
                    break
    
    if not target_record:
        target_record = {
            "khasra_no": khasra_no or "105",
            "khata_no": payload.get("khata_no", "78"),
            "village": village or "Rampur",
            "district": payload.get("district", "Varanasi"),
            "state": payload.get("state", "Uttar Pradesh"),
            "area_sq_meters": float(payload.get("area_sq_meters", 2400.0)),
            "land_type": payload.get("land_type", "Agricultural"),
            "owners": payload.get("owners", [{"name": payload.get("owner_name", "Registered Landowner"), "share_percentage": 100.0}])
        }

    insights = generate_gemini_document_insights(
        parsed_record=target_record,
        raw_text=payload.get("raw_text", ""),
        filename=payload.get("filename", f"Deed_Khasra_{target_record.get('khasra_no')}.pdf"),
        api_key=payload.get("api_key")
    )
    
    return {
        "success": True,
        "record_id": target_record.get("id"),
        "khasra_no": target_record.get("khasra_no"),
        "insights": insights
    }




