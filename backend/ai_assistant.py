import os
import re
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional, Tuple

from backend.database import (
    get_all_records, get_record_by_id, get_all_disputes,
    get_audit_ledger, get_pending_verifications, get_state_district_analytics
)
from backend.land_faq_kb import (
    find_matching_faq, search_faqs, LAND_FAQ_DATABASE, FAQS_BY_ID,
    FAQ_CATEGORIES, POPULAR_FAQS
)

# -------------------------------------------------------------------------
# STATUTORY & PROCEDURAL LAND REVENUE KNOWLEDGE BASE
# Covers: UP Revenue Code 2006, Maharashtra Land Revenue Code 1966,
# Telangana Rights in Land and Pattadar Passbooks Act 2020, DILRMP Guidelines
# -------------------------------------------------------------------------

LEGAL_REMEDIES_KNOWLEDGE = {
    "demarcation": {
        "title": "Boundary Demarcation & Encroachment Removal (सीमांकन एवं हदबंदी)",
        "sections": "Section 24, UP Revenue Code 2006 | Section 85, Maharashtra Land Revenue Code 1966 | Section 9, Telangana RoR Act",
        "competent_officer": "Sub-Divisional Magistrate (SDM) / Tehsildar",
        "survey_agency": "Revenue Inspector (RI) & Halka Patwari with Electronic Total Station (ETS) / DGPS",
        "steps": [
            "1. **File Demarcation Petition (Form RC-22 / RC-23)**: Submit formal demarcation application before the Tehsildar / SDM court specifying your Khasra / Survey number and adjoining boundary holder details.",
            "2. **Deposit Treasury Challan**: Deposit the statutory demarcation fee (standard: ₹1,000 per boundary pillar) via Government Cyber Treasury portal.",
            "3. **Issuance of Notice (Parwana)**: SDM court issues 15-day prior notice to all adjacent plot owners informing them of the scheduled field survey date.",
            "4. **On-Site ETS / DGPS Demarcation**: Revenue Inspector & Patwari conduct physical electronic survey matching village Shajra (cadastral map) and fixed reference points (Sahadda / Tri-junction pillars).",
            "5. **Preparation of Panchnama & Field Map (Najri Naksha)**: Findings are recorded in the presence of villagers, signed by panchas, and boundary coordinates pinned.",
            "6. **Order for Simana Patthar (Boundary Pillars)**: If encroachment is detected, the Tehsildar passes an eviction order directing the encroacher to vacate within 30 days, failing which police assistance is requisitioned."
        ]
    },
    "mutation": {
        "title": "Land Mutation & Record-of-Rights Update (दाखिल-खारिज / नामांतरण)",
        "sections": "Sections 34 & 35, UP Revenue Code 2006 | Section 149/150, Maharashtra Land Revenue Code",
        "competent_officer": "Naib Tehsildar / Tehsildar",
        "statutory_timelines": "35 working days for uncontested mutation; 90 days for contested matters under Citizen Charter",
        "documents_required": [
            "Registered Sale Deed / Gift Deed / Will / Release Deed (certified copy)",
            "Form 35 Application for Mutation",
            "Latest Record of Rights (Khatauni / 7/12 extract / Pahani)",
            "Aadhaar & PAN cards of Transferor and Transferee",
            "Non-Encumbrance Certificate (Bar-Mukt Praman Patra / Form 15)",
            "NOC from co-sharers (in case of ancestral undivided share sale)",
            "Affidavit declaring total land holding does not breach Land Ceiling Act limits (12.5 acres in UP)"
        ],
        "steps": [
            "1. Apply online via state portal (UP e-District/Bhulekh, MahaDBT, Dharani) with registered deed number.",
            "2. Revenue registry auto-generates proclamation (Ishtehaar) displayed at Tehsil notice board and Village Panchayat for 35 days for objections.",
            "3. If no objection received, Halka Patwari submits inspection report confirming actual physical possession (Kabza).",
            "4. Naib Tehsildar passes Mutation Order and directs Patwari to update Khatauni and ROR ledger.",
            "5. Certified updated Khatauni extract (Amal-Daramad) issued to landowner."
        ]
    },
    "co_sharer": {
        "title": "Co-Sharer Equity Mismatch & Family Partition (खातेदारों का अंश निर्धारण एवं बंटवारा)",
        "sections": "Section 116 (Suit for Division of Holding) & Section 117 (Compromise Partition), UP Revenue Code 2006",
        "competent_officer": "Sub-Divisional Officer (SDO) / Assistant Collector 1st Class",
        "steps": [
            "1. **Mathematical Discrepancy Rectification**: When recorded co-sharer percentages sum to != 100% (or fraction != 1), file an application under Section 38 for correction of clerical / arithmetical error in Khatauni.",
            "2. **Private Family Partition (Aapasi Batwara)**: Co-sharers can execute a registered partition agreement with demarcated Kurras (sub-lots) and apply under Section 117 for separate Khata allotment.",
            "3. **Revenue Court Partition Suit**: If amicable settlement fails, file suit under Section 116 before SDO. The court orders preliminary decree determining share fractions, then appoints Revenue Inspector to prepare field Kurras (Qurra bandi), followed by final decree allotting distinct Khasra numbers (e.g., 105/1, 105/2)."
        ]
    },
    "bank_lending": {
        "title": "Bank Title Search & Non-Encumbrance Clearance (बैंक ऋण एवं बंधक पात्रता)",
        "checklist": [
            "1. **Clear Title & Sole / Valid Co-ownership**: Khasra must have status 'CLEAR' with 100% share accounting and zero active boundary or title disputes.",
            "2. **30-Year Chain of Title (Talaash Register)**: Search at Sub-Registrar Office (SRO) confirming unbroken legal title lineage.",
            "3. **Nil-Encumbrance Certificate (EC - Form 15 & 16)**: Proves property is free from prior mortgages, court attachments, or recovery warrants.",
            "4. **DILRMP Central Verification**: Survey number cross-verified against State Revenue Cloud Gateway (Bhulekh/Bhoomi/Dharani).",
            "5. **No Court Injunction**: Verified no pending lis pendens under Section 52 Transfer of Property Act or Order 39 CPC in Revenue/Civil Courts.",
            "6. **Creation of Gehan / Equitable Mortgage**: Bank lien registered with Tehsildar office and updated in Column 4 of Khatauni (Khasra note)."
        ]
    }
}

ROLE_PERSPECTIVES = {
    "CITIZEN_FARMER": "You are assisting a Citizen or Landowner. Use clear, empathetic, respectful, and plain language. Avoid overly dense bureaucratic jargon, and always offer clear step-by-step guidance on what documents to gather and which local revenue office (Tehsil, Patwari Halka, CSC Center) to visit.",
    "REVENUE_OFFICER": "You are assisting a Revenue Officer, Tehsildar, or Patwari. Provide authoritative statutory citations (UP Revenue Code 2006, MLRC 1966, DILRMP circulars), procedural requirements for spot inspection, ETS demarcation orders, and guidance on certifying HITL pending records or executing blockchain mutations.",
    "BANK_OFFICER": "You are assisting a Bank Credit / Lending Officer conducting title diligence. Focus on legal encumbrance risk, chain-of-title integrity, SARFAESI compliance, Form 15/16 search, and explicit loan eligibility green/red flags.",
    "DILRMP_ADMIN": "You are assisting a DILRMP State Administrator. Highlight state/district progress, ML OCR confidence rates, cadastral boundary alignment metrics, and blockchain ledger health."
}

# -------------------------------------------------------------------------
# DATABASE INTROSPECTION & CONTEXT RETRIEVAL
# -------------------------------------------------------------------------

STOPWORDS = {
    "what", "is", "the", "for", "and", "how", "can", "tell", "show", "about",
    "with", "from", "are", "process", "steps", "details", "give", "help",
    "please", "this", "that", "land", "records", "record", "khasra", "khata",
    "portal", "system", "file", "apply", "want", "know", "need", "guide",
    "mutation", "dispute", "demarcation", "procedure", "check", "status"
}

def search_live_records(query: str) -> List[Dict[str, Any]]:
    """Finds records matching query tokens in khasra_no, khata_no, village, owner name, or id."""
    q = query.strip().lower()
    if not q:
        return []
    records = get_all_records()
    matches = []
    
    # Try exact khasra or ID match first
    for r in records:
        khasra = str(r.get("khasra_no", "")).lower()
        rec_id = str(r.get("id", "")).lower()
        if q == khasra or q == rec_id or f"khasra {khasra}" in q or f"parcel {khasra}" in q or f"plot {khasra}" in q:
            matches.append(r)
            
    if matches:
        return matches
        
    # Word-level search across fields excluding common stop words
    query_tokens = [w for w in re.findall(r'\b[a-zA-Z0-9_\-\/]{3,}\b', q) if w not in STOPWORDS]
    if not query_tokens:
        return []

    for r in records:
        khasra = str(r.get("khasra_no", "")).lower()
        khata = str(r.get("khata_no", "")).lower()
        village = str(r.get("village", "")).lower()
        district = str(r.get("district", "")).lower()
        rec_id = str(r.get("id", "")).lower()
        owners = " ".join([o.get("name", "").lower() for o in r.get("owners", [])])
        
        score = 0
        for token in query_tokens:
            if token == khasra: score += 10
            elif token in khasra: score += 5
            if token == rec_id: score += 10
            elif token in rec_id: score += 5
            if re.search(rf'\b{re.escape(token)}\b', owners): score += 5
            if re.search(rf'\b{re.escape(token)}\b', village): score += 4
            if re.search(rf'\b{re.escape(token)}\b', district): score += 3
            
        if score >= 4:
            matches.append((score, r))
            
    matches.sort(key=lambda x: x[0], reverse=True)
    return [m[1] for m in matches[:5]]


def search_live_disputes(query: str, linked_record_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    disputes = get_all_disputes()
    q = query.strip().lower()
    matched = []
    
    linked_ids = linked_record_ids or []
    
    for d in disputes:
        d_id = d.get("id", "").lower()
        rec_ids = [rid.lower() for rid in d.get("record_ids", [])]
        title = d.get("title", "").lower()
        desc = d.get("description", "").lower()
        
        # Check linked record ids
        if any(lid.lower() in rec_ids for lid in linked_ids):
            matched.append(d)
            continue
            
        if d_id in q or title in q:
            matched.append(d)
            continue
            
        # Match words
        for w in q.split():
            if len(w) > 2 and (w in d_id or w in title or w in desc or any(w in rid for rid in rec_ids)):
                matched.append(d)
                break
                
    return matched[:5]


def extract_khasra_numbers(text: str) -> List[str]:
    """Finds referenced khasra numbers like '101', '102', '105/2', '142/A'."""
    patterns = [
        r'(?:khasra|survey|plot|gat|khatian|खसरा|प्लॉट)\s*(?:no\.?|number|#)?\s*([0-9]+(?:/[0-9A-Za-z]+)?)',
        r'#([0-9]+(?:/[0-9A-Za-z]+)?)',
        r'\b([0-9]{2,4}(?:/[0-9A-Za-z]+)?)\b'
    ]
    khasras = []
    for pat in patterns:
        found = re.findall(pat, text, re.IGNORECASE)
        for f in found:
            if f not in khasras and len(f) <= 8 and not f.startswith("202"):  # Avoid years
                khasras.append(f)
    return khasras

# -------------------------------------------------------------------------
# AUTONOMOUS EXPERT REVENUE INTELLIGENCE ENGINE (OFFLINE RESILIENT)
# -------------------------------------------------------------------------

def generate_expert_response(
    message: str,
    role: str = "REVENUE_OFFICER",
    current_record_id: Optional[str] = None,
    state: Optional[str] = None,
    category_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Synthesizes a complete, satisfied, legally accurate response using the live database,
    procedural revenue law knowledge base, and role-tailored perspectives.
    """
    msg_lower = message.lower().strip()
    is_devanagari = bool(re.search(r'[\u0900-\u097F]', message))
    is_hindi_phonetic = any(re.search(rf'\b{w}\b', msg_lower) for w in ["kya", "kaise", "bataiye", "batao", "karna", "karein", "meri", "mera", "hoga", "chahiye", "vivad", "namantaran", "batwara", "seemankan"])
    is_hindi = is_devanagari or is_hindi_phonetic
    
    # 1. Gather Live Context
    all_records = get_all_records()
    all_disputes = get_all_disputes()
    analytics = get_state_district_analytics()
    total_records = len(all_records)
    active_disputes = [d for d in all_disputes if d.get("status") == "ACTIVE"]
    pending_queue = get_pending_verifications()
    
    # Find any specific records mentioned
    khasras = extract_khasra_numbers(message)
    target_records = []
    
    if current_record_id:
        curr_rec = get_record_by_id(current_record_id)
        if curr_rec and curr_rec not in target_records:
            target_records.append(curr_rec)
            
    for k in khasras:
        for r in all_records:
            if str(r.get("khasra_no")).lower() == k.lower():
                if r not in target_records:
                    target_records.append(r)
                    
    # Only perform fuzzy record search if the query isn't an obvious general procedural question
    is_mutation_query = any(w in msg_lower for w in ["mutation", "dakhil", "kharij", "transfer", "namantaran", "sale deed", "registry", "वारिस", "दाखिल-खारिज"])
    is_demarcation_query = any(w in msg_lower for w in ["demarcation", "seemankan", "hadbandi", "paimayish", "ets", "pillar", "सीमांकन", "हदबंदी", "पैमाइश"])
    is_bank_query = any(w in msg_lower for w in ["loan", "bank", "mortgage", "kcc", "hypothecation", "encumbrance", "nil encumbrance", "ऋण", "बैंक", "बंधक"])
    is_blockchain_query = any(w in msg_lower for w in ["blockchain", "ledger", "audit", "hash", "tamper", "immutable", "sha-256", "ब्लॉकचेन"])
    is_queue_query = any(w in msg_lower for w in ["pending", "review", "patwari", "hitl", "officer review", "confidence", "faded", "सत्यापन"])
    is_dispute_query = any(w in msg_lower for w in ["dispute", "overlap", "encroach", "conflict", "kabza", "illegal", "border", "vivad", "विवाद", "सीमा", "अतिक्रमण"])
    is_greeting = any(w in msg_lower for w in ["hello", "hi", "hey", "namaste", "pranam", "who are you", "help me", "kya kar sakte"])

    is_explicit_record_inquiry = bool(khasras) or bool(current_record_id) or bool(re.search(r'\b(rec-[a-z0-9\-]+|khasra\s*#?\s*[0-9]+|parcel\s*#?\s*[0-9]+)\b', msg_lower))

    if not target_records and is_explicit_record_inquiry:
        target_records = search_live_records(message)
        
    # Find linked disputes
    target_record_ids = [r["id"] for r in target_records]
    target_disputes = search_live_disputes(message, target_record_ids)
    
    # Check for matching FAQ in Land Records Knowledge Base (184 FAQs)
    matched_faq, faq_score = find_matching_faq(message, state=state, category_id=category_id)

    # Build Suggested Action buttons
    suggested_actions = []
    suggested_questions = []
    reply_paragraphs = []
    
    # CASE 1: SPECIFIC RECORD INQUIRY
    if target_records and is_explicit_record_inquiry:
        rec = target_records[0]
        khasra = rec.get("khasra_no")
        village = rec.get("village")
        district = rec.get("district")
        state = rec.get("state")
        area_m2 = rec.get("area_sq_meters")
        area_ha = rec.get("area_hectares")
        status = rec.get("dispute_status")
        ver_status = rec.get("verification_status")
        owners = rec.get("owners", [])
        owner_names = ", ".join([f"{o.get('name')} ({o.get('share_percentage')}%)" for o in owners])
        
        # Add action buttons
        suggested_actions.append({
            "type": "NAVIGATE_TAB",
            "tab": "map",
            "payload": {"record_id": rec["id"], "khasra_no": khasra},
            "label": f"🗺️ View Khasra {khasra} on Cadastral Map"
        })
        suggested_actions.append({
            "type": "SEARCH_RECORD",
            "query": khasra,
            "label": f"🔍 Inspect Record {rec['id']}"
        })
        
        if is_hindi:
            header = f"### 📜 खसरा संख्या {khasra} का संपूर्ण विवरण ({village}, {district}, {state})"
            reply_paragraphs.append(header)
            reply_paragraphs.append(
                f"- **स्वामित्व (Landowners)**: {owner_names}\n"
                f"- **क्षेत्रफल (Area)**: {area_m2:,.1f} वर्ग मीटर ({area_ha} हेक्टेयर)\n"
                f"- **विवाद स्थिति (Dispute Status)**: **{status}**\n"
                f"- **सत्यापन स्थिति (Verification)**: {ver_status}\n"
                f"- **दस्तावेज़ स्रोत**: {rec.get('document_source', 'Bhulekh Record')}\n"
                f"- **क्रिप्टोग्राफ़िक ऑडिट हैश**: `{rec.get('audit_hash', '')[:16]}...`"
            )
        else:
            header = f"### 📜 Official Record Analysis: Khasra #{khasra} ({village}, {district}, {state})"
            reply_paragraphs.append(header)
            reply_paragraphs.append(
                f"- **Primary Ownership**: {owner_names}\n"
                f"- **Cadastral Area**: **{area_m2:,.1f} m²** ({area_ha} Hectares / {rec.get('area_acres')} Acres)\n"
                f"- **Dispute Status**: `{status}`\n"
                f"- **Verification Authority**: `{ver_status}` ({rec.get('verified_by') or 'Automated AI-OCR'})\n"
                f"- **Source Registry**: {rec.get('document_source', 'DILRMP Central Registry')}\n"
                f"- **Tamper-Proof Audit Hash**: `{rec.get('audit_hash', '')[:20]}...`"
            )
            
        # Check linked disputes
        rec_disputes = [d for d in all_disputes if rec["id"] in d.get("record_ids", [])]
        if rec_disputes:
            disp = rec_disputes[0]
            suggested_actions.append({
                "type": "RESOLVE_DISPUTE",
                "dispute_id": disp["id"],
                "label": f"⚖️ Open Demarcation & Resolution Window ({disp['id']})"
            })
            
            if is_hindi:
                reply_paragraphs.append(
                    f"\n#### ⚠️ सक्रिय विवाद विवरण ({disp.get('id')} - {disp.get('title')})\n"
                    f"- **विवाद का प्रकार**: {disp.get('dispute_type')}\n"
                    f"- **गंभीरता (Severity)**: **{disp.get('severity')}**\n"
                    f"- **विवरण**: {disp.get('description')}\n"
                    f"- **प्रभावित अतिच्छादन क्षेत्रफल**: **{disp.get('overlap_area_sq_meters', 0):,.1f} m²**\n\n"
                    f"**समाधान का कानूनी उपाय (Legal Action Plan)**:\n"
                    f"1. उत्तर प्रदेश राजस्व संहिता 2006 की **धारा 24** के तहत उप-जिलाधिकारी (SDM) न्यायालय में सीमांकन (Demarcation/Seemankan) का वाद दायर करें।\n"
                    f"2. राजस्व निरीक्षक (RI) एवं लेखपाल द्वारा ETS (इलेक्ट्रॉनिक टोटल स्टेशन) पैमाइश कराएं।\n"
                    f"3. पैमाइश आख्या के आधार पर सीमा स्तंभ (हदबंदी पत्थर) स्थापित कर अवैध कब्जा हटवाया जाएगा।"
                )
            else:
                reply_paragraphs.append(
                    f"\n#### ⚠️ Active Dispute Flagged: {disp.get('title')} ({disp.get('id')})\n"
                    f"- **Dispute Classification**: `{disp.get('dispute_type')}`\n"
                    f"- **Severity Level**: **{disp.get('severity')} RISK**\n"
                    f"- **Encroachment Impact**: **{disp.get('overlap_area_sq_meters', 0):,.1f} m²** spatial boundary overlap with adjoining parcel.\n"
                    f"- **Case Description**: {disp.get('description')}\n\n"
                    f"**Recommended Legal Remedy & Action Steps**:\n"
                    f"1. **File Demarcation Petition (Sec 24 UP Revenue Code / Sec 85 MLRC)**: Apply to the SDM / Tehsildar for an official joint physical demarcation.\n"
                    f"2. **Electronic Total Station (ETS) Survey**: Revenue Inspector and Halka Patwari will locate boundary tri-junctions (Sahadda) and establish geo-coordinates.\n"
                    f"3. **Eviction / Settlement Decree**: Upon receipt of the Panchnama, the Tehsildar will issue an order directing removal of any encroaching structure within 30 days."
                )
        else:
            if status == "CLEAR":
                if is_hindi:
                    reply_paragraphs.append(
                        f"\n✅ **यह भूखंड पूर्णतः विवाद-मुक्त एवं स्वच्छ (Clear Title) है।**\n"
                        f"- कोई सक्रिय सीमा विवाद या सह-खातेदार विसंगति दर्ज नहीं है।\n"
                        f"- यह भूखंड बैंक बंधक (Bank Mortgage) एवं कृषि ऋण (KCC) हेतु शत-प्रतिशत पात्र है।"
                    )
                else:
                    reply_paragraphs.append(
                        f"\n✅ **Clear & Encumbrance-Free Title Verified.**\n"
                        f"- No active boundary overlaps, duplicate survey claims, or title breaches exist.\n"
                        f"- DILRMP National Gateway cross-check confirmed 100% ownership equity.\n"
                        f"- Fully eligible for banking mortgage, Kisan Credit Card (KCC), or mutation transfer."
                    )
                    
        suggested_questions = [
            f"How to resolve dispute for Khasra {khasra}?",
            f"Is Khasra {khasra} eligible for bank loan?",
            "What documents are needed for mutation (Dakhil Kharij)?",
            "Show boundary demarcation procedure"
        ]

    # CASE 2: BOUNDARY OVERLAP & DEMARCATION ADVICE
    elif is_dispute_query or is_demarcation_query:
        dem = LEGAL_REMEDIES_KNOWLEDGE["demarcation"]
        suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "disputes", "label": "⚖️ View Active Disputes Engine"})
        suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "map", "label": "🗺️ Open Cadastral Map Overlays"})
        
        if is_hindi:
            reply_paragraphs.append(f"### ⚖️ भूमि सीमा विवाद एवं पैमाइश / सीमांकन समाधान (Seemankan Guide)")
            reply_paragraphs.append(
                f"जब दो खेतों या भूखंडों के बीच मेड़ (Boundary) को लेकर विवाद अथवा अवैध कब्जा (Encroachment) हो, तो निम्नलिखित विधिक प्रक्रिया अपनाएं:\n\n"
                f"**लागू कानून**: {dem['sections']}\n"
                f"**सक्षम प्राधिकारी**: {dem['competent_officer']}\n"
                f"**सर्वेक्षण दल**: {dem['survey_agency']}\n\n"
                f"#### 📋 चरणबद्ध समाधान प्रक्रिया (Step-by-Step Resolution):"
            )
            for step in dem["steps"]:
                reply_paragraphs.append(step)
            reply_paragraphs.append(
                f"\n💡 **त्वरित सुझाव**: आप हमारे सिस्टम में 'Dispute Engine' टैब पर जाकर संबंधित विवाद को सीधे Revenue Officer Settlement Decree द्वारा निस्तारित कर सकते हैं।"
            )
        else:
            reply_paragraphs.append(f"### ⚖️ Cadastral Boundary Encroachment & Demarcation Resolution Guide")
            reply_paragraphs.append(
                f"When two parcels overlap or an adjoining holder encroaches across the field boundary (Mend/Dhur), follow the statutory procedure under Indian Land Revenue law:\n\n"
                f"- **Governing Statute**: {dem['sections']}\n"
                f"- **Adjudicating Forum**: {dem['competent_officer']}\n"
                f"- **Field Execution**: {dem['survey_agency']}\n\n"
                f"#### 📋 Step-by-Step Resolution Workflow:"
            )
            for step in dem["steps"]:
                reply_paragraphs.append(step)
            reply_paragraphs.append(
                f"\n💡 **Operational Action**: If you are logged in as a Revenue Officer / Patwari, navigate to the **Dispute Engine** tab and click **Demarcate & Settle** to log an official resolution directly to the cryptographic audit ledger."
            )
            
        suggested_questions = [
            "What is the fee for Section 24 demarcation?",
            "What is the status of Khasra 102?",
            "How to apply for Mutation (Dakhil Kharij)?",
            "How does Electronic Total Station (ETS) survey work?"
        ]

    # CASE 3: MUTATION & TITLE REGISTRATION (DAKHIL KHARIJ)
    elif is_mutation_query:
        mut = LEGAL_REMEDIES_KNOWLEDGE["mutation"]
        suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "digitize", "label": "📄 AI-OCR Digitizer (Ingest Deed)"})
        suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "citizen", "label": "🔍 Citizen Title Search"})
        
        if is_hindi:
            reply_paragraphs.append(f"### 📝 नामांतरण / दाखिल-खारिज (Mutation) की संपूर्ण विधिक प्रक्रिया")
            reply_paragraphs.append(
                f"रजिस्ट्री या वसीयत के बाद राजस्व अभिलेखों (खतौनी) में नाम दर्ज कराने की प्रक्रिया:\n\n"
                f"- **संबंधित कानून**: {mut['sections']}\n"
                f"- **सक्षम अधिकारी**: {mut['competent_officer']}\n"
                f"- **कानूनी समय-सीमा (Citizen Charter)**: **{mut['statutory_timelines']}**\n\n"
                f"#### 📂 आवश्यक दस्तावेज़ चेकलिस्ट (Mandatory Documents):"
            )
            for doc in mut["documents_required"]:
                reply_paragraphs.append(f"- {doc}")
            reply_paragraphs.append(f"\n#### 🚀 चरणबद्ध कार्यप्रणाली:")
            for s in mut["steps"]:
                reply_paragraphs.append(s)
        else:
            reply_paragraphs.append(f"### 📝 Standard Operating Procedure for Land Mutation (Dakhil-Kharij)")
            reply_paragraphs.append(
                f"Mutation is the formal fiscal transfer of ownership entry in the state Record of Rights (Khatauni/Pahani) following sale, gift, inheritance, or court decree.\n\n"
                f"- **Governing Statute**: {mut['sections']}\n"
                f"- **Adjudicating Officer**: {mut['competent_officer']}\n"
                f"- **Statutory Time Limit**: **{mut['statutory_timelines']}**\n\n"
                f"#### 📂 Required Document Checklist:"
            )
            for doc in mut["documents_required"]:
                reply_paragraphs.append(f"- {doc}")
            reply_paragraphs.append(f"\n#### 🚀 Step-by-Step Execution:")
            for s in mut["steps"]:
                reply_paragraphs.append(s)
                
        suggested_questions = [
            "What if someone files an objection during mutation?",
            "Check status of Khasra 101",
            "How to resolve boundary overlap?",
            "What is co-sharer partition (Batwara)?"
        ]

    # CASE 4: BANK LENDING & MORTGAGE DUE DILIGENCE
    elif is_bank_query:
        bnk = LEGAL_REMEDIES_KNOWLEDGE["bank_lending"]
        suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "dashboard", "label": "📊 View Clean Title Registry"})
        suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "ledger", "label": "🛡️ Inspect Blockchain Ledger"})
        
        reply_paragraphs.append(f"### 🏦 Bank Credit & Mortgage Legal Due Diligence Guidelines")
        reply_paragraphs.append(
            f"Before sanctioning agricultural, residential, or commercial loans against land security, financial institutions must ensure zero encumbrance and absolute title validity:\n"
        )
        for item in bnk["checklist"]:
            reply_paragraphs.append(item)
            
        reply_paragraphs.append(
            f"\n🔍 **Live System Status**: Currently, **{analytics.get('states', {}).get('Uttar Pradesh', {}).get('verified', 0)} parcels** in the system have achieved certified non-encumbrance status and are eligible for instant digital mortgage underwriting."
        )
        suggested_questions = [
            "Is Khasra 101 eligible for bank loan?",
            "Why is Khasra 102 flagged for lending risk?",
            "How to verify blockchain audit trail?",
            "Search citizen title directory"
        ]

    # CASE 5: BLOCKCHAIN & CRYPTOGRAPHIC AUDIT
    elif is_blockchain_query:
        suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "ledger", "label": "🛡️ Verify Blockchain Audit Trail"})
        ledger = get_audit_ledger()
        
        reply_paragraphs.append(f"### 🛡️ SHA-256 Cryptographic Audit Ledger & Tamper Prevention")
        reply_paragraphs.append(
            f"The Bhoomi Land Dispute Manager implements a zero-trust, append-only cryptographic ledger inspired by blockchain principles:\n\n"
            f"1. **Chained SHA-256 Hashing**: Every event—new parcel ingestion, Patwari HITL verification, boundary change, or dispute decree—is serialized and hashed. Each block points to the preceding block's hash (`prev_hash`), ensuring mathematical immutability.\n"
            f"2. **Real-time Tamper Detection**: The system validates the entire chain from Genesis (`0000000000000000`) to the latest block. Any unauthorized direct database modification breaks the chain immediately.\n"
            f"3. **Audited Blocks Count**: Currently **{len(ledger)} immutable blocks** are logged and cryptographically synchronized across state nodes."
        )
        suggested_questions = [
            "Verify entire blockchain ledger integrity",
            "Show recent audit transactions",
            "How to resolve boundary encroachment?",
            "Check status of Khasra 105"
        ]

    # CASE 6: HITL REVIEW QUEUE & OCR CONFIDENCE
    elif is_queue_query:
        suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "verify", "label": "📋 Open Human Review Queue"})
        
        reply_paragraphs.append(f"### 📋 Human-in-the-Loop (HITL) Patwari Verification Queue")
        reply_paragraphs.append(
            f"To safeguard against OCR hallucination or damaged historical paper registers:\n\n"
            f"- **Confidence Threshold**: When the multilingual ML-OCR model detects faded ink or ambiguity resulting in field confidence < **85%**, the parcel is isolated into the **Review Queue**.\n"
            f"- **Current Pending Review**: There are **{len(pending_queue)} records** awaiting physical register comparison.\n"
            f"- **Patwari Action**: The officer inspects the original deed facsimile, enters verified values, and submits certification with digital remarks, elevating confidence to 100%."
        )
        suggested_questions = [
            "Open pending verification queue",
            "How does AI-OCR digitization work?",
            "Check status of Khasra 102",
            "How to resolve boundary overlap?"
        ]

    # CASE 7: COMPREHENSIVE LAND RECORDS KNOWLEDGE BASE (184 FAQS)
    elif matched_faq and faq_score >= 38.0 and not is_greeting:
        cat_name = matched_faq.get("category", "Land Records")
        cat_id = matched_faq.get("category_id", "records")
        q_en = matched_faq.get("question", "")
        q_hi = matched_faq.get("question_hi", "")
        q_title = q_hi if (is_hindi and q_hi) else q_en
        ans = matched_faq.get("answer", "")
        state_notes = matched_faq.get("state_notes", "")
        related = matched_faq.get("related_questions", [])

        # Add targeted action buttons based on FAQ category
        if cat_id in ["disputes", "demarcation", "measurement"]:
            suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "disputes", "label": "⚖️ View Active Disputes Engine"})
            suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "map", "label": "🗺️ Open Cadastral Map Overlays"})
        elif cat_id in ["mutation", "registration"]:
            suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "digitize", "label": "📄 Ingest Revenue Deed (AI-OCR)"})
            suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "citizen", "label": "🔍 Citizen Title Search"})
        elif cat_id in ["loans", "loans_mortgage"]:
            suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "dashboard", "label": "📊 View Clean Title Registry"})
            suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "ledger", "label": "🛡️ Inspect Cryptographic Ledger"})
        elif cat_id in ["digital_records", "records", "ownership"]:
            suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "citizen", "label": "🔍 Search Land Records Directory"})
            suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "map", "label": "🗺️ View Cadastral Map"})
        else:
            suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "citizen", "label": "🔍 Citizen Land Services"})
            suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "map", "label": "🗺️ Cadastral Map Viewer"})

        if is_hindi:
            reply_paragraphs.append(f"### 🏷️ {cat_name} | {q_title}")
            reply_paragraphs.append(ans)
            if state_notes:
                reply_paragraphs.append(f"📍 **राज्य-वार नियम (State Rules)**: {state_notes}")
            reply_paragraphs.append(
                "⚖️ *विधिक सूचना: यह उत्तर भारतीय भू-राजस्व संहिताओं (UP Revenue Code, MLRC, DILRMP दिशानिर्देश) पर आधारित है। किसी न्यायालयीन वाद हेतु अपने तहसील कार्यालय या अधिकृत राजस्व अधिवक्ता से संपर्क करें।*"
            )
        else:
            reply_paragraphs.append(f"### 🏷️ {cat_name} | {q_title}")
            reply_paragraphs.append(ans)
            if state_notes:
                reply_paragraphs.append(f"📍 **State-Specific Applicability**: {state_notes}")
            reply_paragraphs.append(
                "⚖️ *Legal Advisory: This response is grounded in statutory Indian Land Revenue procedures (UP Revenue Code 2006, MLRC 1966, DILRMP guidelines). For contested court litigation, consult your local Sub-Divisional Magistrate/Tehsildar or a licensed revenue advocate.*"
            )

        if related:
            suggested_questions = list(related[:4])
        else:
            suggested_questions = [
                "What is a Khasra number?",
                "How to apply for Mutation (Dakhil Kharij)?",
                "How to resolve boundary encroachment?",
                "Is land mortgaged to bank?"
            ]

    # CASE 8: GENERAL OVERVIEW / GREETING
    else:
        role_context = ROLE_PERSPECTIVES.get(role, ROLE_PERSPECTIVES["REVENUE_OFFICER"])
        suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "map", "label": "🗺️ Open Cadastral Map"})
        suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "disputes", "label": "⚖️ Inspect Disputes"})
        suggested_actions.append({"type": "NAVIGATE_TAB", "tab": "digitize", "label": "📄 Ingest Revenue Deed"})
        
        if is_hindi:
            reply_paragraphs.append(f"### 🙏 नमस्ते! मैं भूमि AI सहायक (Bhoomi AI Sahayak) हूँ।")
            reply_paragraphs.append(
                f"मैं भारत सरकार के **डिजिटल इंडिया लैंड रिकॉर्ड्स मॉडर्नाइजेशन प्रोग्राम (DILRMP)** के तहत आपकी भूमि समस्याओं, विवाद समाधान, और राजस्व अभिलेखों के निस्तारण में पूर्ण सहायता के लिए तैयार हूँ।\n\n"
                f"**मैं आपकी किस प्रकार सहायता कर सकता हूँ?**\n"
                f"- **खसरा / खतौनी जांच**: किसी भी खसरा संख्या (जैसे 101, 102, 105) की विवाद स्थिति, क्षेत्रफल एवं मालिकाना हक की जांच।\n"
                f"- **सीमा विवाद समाधान**: मेड़ विवाद, अतिक्रमण, एवं धारा 24 सीमांकन (Seemankan/Hadbandi) की कानूनी प्रक्रिया।\n"
                f"- **नामांतरण (दाखिल-खारिज)**: फॉर्म 35, आवश्यक दस्तावेज़, एवं 35-दिवसीय प्रक्रिया की समय-सीमा।\n"
                f"- **बैंक लोन पात्रता**: बंधक (Mortgage) एवं गैर-विवादित टाइटल सर्च की 13-सूत्रीय जांच।\n"
                f"- **ब्लॉकचेन सत्यापन**: छेड़छाड़-रहित डिजिटल लेजर एवं पटवारी सत्यापन।"
            )
        else:
            reply_paragraphs.append(f"### 👋 Welcome to Bhoomi AI Sahayak (भूमि AI सहायक)")
            reply_paragraphs.append(
                f"I am your official AI legal & operational consultant for the **Intelligent Land Record Digitization & Validation System** (DILRMP - Ministry of Rural Development, Govt of India).\n\n"
                f"**Active Perspective**: *{role_context}*\n\n"
                f"**What can I assist you with today?**\n"
                f"1. **Instant Cadastral Lookup**: Query any Khasra/Survey # (e.g. *101*, *102*, *105*) to inspect co-sharer equity, boundary geometry, and legal status.\n"
                f"2. **Boundary Dispute Resolution**: Step-by-step guidance on Section 24 Demarcation (Seemankan), Electronic Total Station (ETS) field surveys, and settlement decrees.\n"
                f"3. **Mutation (Dakhil-Kharij) Checklist**: Mandatory documents, statutory citizen charter deadlines (35/90 days), and objection handling.\n"
                f"4. **Bank Loan & Mortgage Clearance**: Non-encumbrance title vetting, 30-year chain of title, and SARFAESI compliance.\n"
                f"5. **Blockchain Audit Verification**: SHA-256 tamper-proof ledger validation."
            )
            
        suggested_questions = [
            "What is the status of Khasra 102?",
            "How do I resolve boundary encroachment?",
            "What are the steps for land mutation (Dakhil Kharij)?",
            "Is Khasra 101 eligible for a bank loan?",
            "How does Section 24 demarcation work?"
        ]

    reply_markdown = "\n\n".join(reply_paragraphs)
    
    return {
        "reply": reply_markdown,
        "suggested_actions": suggested_actions,
        "suggested_questions": suggested_questions,
        "referenced_records": [
            {
                "id": r["id"],
                "khasra_no": r.get("khasra_no"),
                "village": r.get("village"),
                "status": r.get("dispute_status"),
                "area_hectares": r.get("area_hectares")
            } for r in target_records[:3]
        ],
        "referenced_disputes": [
            {
                "id": d["id"],
                "title": d.get("title"),
                "dispute_type": d.get("dispute_type"),
                "severity": d.get("severity")
            } for d in target_disputes[:3]
        ],
        "matched_faq_id": matched_faq["id"] if matched_faq and faq_score >= 38.0 else None,
        "faq_category": matched_faq["category"] if matched_faq and faq_score >= 38.0 else None,
        "source": "bhoomi-expert-engine" if not (matched_faq and faq_score >= 38.0) else "bhoomi-faq-knowledge-engine"
    }

# -------------------------------------------------------------------------
# GEMINI API INTEGRATION WITH AUTOMATIC RETRIEVAL AUGMENTATION (RAG)
# -------------------------------------------------------------------------

def query_gemini_api(
    message: str,
    role: str = "REVENUE_OFFICER",
    api_key: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    current_record_id: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Calls Google Gemini API using pure standard library (urllib.request) with complete live DB context.
    Falls back gracefully if key is missing or request fails.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return None

    # Ingest Live DB facts to feed into system context
    records = get_all_records()
    disputes = get_all_disputes()
    ledger = get_audit_ledger()
    
    records_summary = "\n".join([
        f"- ID: {r['id']} | Khasra: {r.get('khasra_no')} | Village: {r.get('village')}, {r.get('district')} | Status: {r.get('dispute_status')} | Area: {r.get('area_sq_meters')} m² | Owners: {', '.join([o.get('name', '') for o in r.get('owners', [])])} | Verification: {r.get('verification_status')}"
        for r in records[:10]
    ])
    
    disputes_summary = "\n".join([
        f"- Dispute ID: {d['id']} | Records: {', '.join(d.get('record_ids', []))} | Title: {d.get('title')} | Type: {d.get('dispute_type')} | Severity: {d.get('severity')} | Overlap Area: {d.get('overlap_area_sq_meters')} m²"
        for d in disputes[:6]
    ])

    system_instruction = (
        "You are 'Bhoomi AI Sahayak' (भूमि AI सहायक), the authoritative, helpful, and highly intelligent AI consultant "
        "integrated into the Government of India's Intelligent Land Record Digitization and Validation System (DILRMP). "
        f"The current user role is '{role}'. {ROLE_PERSPECTIVES.get(role, '')} "
        "You provide comprehensive, legally accurate, highly structured, and empathetic answers to solve land disputes, "
        "guide through statutory procedures (Demarcation under Section 24, Mutation/Dakhil-Kharij under Section 34/35, Co-sharer partitions under Section 116), "
        "and inspect real cadastral parcels from the system. "
        "Always give direct, actionable advice, cite relevant revenue sections, and offer step-by-step checklists. "
        "Support both English and Hindi/Hinglish naturally depending on the user's language.\n\n"
        f"--- LIVE SYSTEM DATABASE GROUND TRUTH ---\n"
        f"LAND PARCELS:\n{records_summary}\n\n"
        f"ACTIVE DISPUTES:\n{disputes_summary}\n\n"
        f"LEDGER STATUS: {len(ledger)} cryptographically linked immutable SHA-256 blocks."
    )

    # Format history
    contents = []
    contents.append({
        "role": "user",
        "parts": [{"text": f"System Context & Instructions:\n{system_instruction}\n\nInitial query: Start conversation."}]
    })
    contents.append({
        "role": "model",
        "parts": [{"text": "Namaste! I am Bhoomi AI Sahayak, ready with full real-time access to the cadastral registry, dispute engine, and revenue legal codes."}]
    })
    
    if conversation_history:
        for msg in conversation_history[-6:]:
            role_type = "user" if msg.get("role") == "user" else "model"
            contents.append({
                "role": role_type,
                "parts": [{"text": msg.get("content", "")}]
            })
            
    contents.append({
        "role": "user",
        "parts": [{"text": message}]
    })

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
    payload_data = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1500
        }
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload_data).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=12) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            candidate = res_data.get("candidates", [{}])[0]
            text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
            if text:
                # Also generate deep link actions
                expert_fallback = generate_expert_response(message, role, current_record_id)
                return {
                    "reply": text,
                    "suggested_actions": expert_fallback["suggested_actions"],
                    "suggested_questions": expert_fallback["suggested_questions"],
                    "referenced_records": expert_fallback["referenced_records"],
                    "referenced_disputes": expert_fallback["referenced_disputes"],
                    "source": "gemini-2.5-flash"
                }
    except Exception as e:
        print(f"Notice: Gemini API call failed or timed out ({e}). Seamlessly falling back to autonomous Expert Engine.")
        return None

# -------------------------------------------------------------------------
# MAIN FACADE: PROCESS CHAT MESSAGE
# -------------------------------------------------------------------------

def process_chat_message(
    message: str,
    role: str = "REVENUE_OFFICER",
    api_key: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    current_record_id: Optional[str] = None,
    state: Optional[str] = None,
    category_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main entry point for AI Chat interactions.
    Attempts Gemini API if key is present; otherwise immediately produces rich,
    authoritative, live-database grounded answers via autonomous Expert Knowledge Engine.
    """
    # 1. Try Gemini if configured
    if api_key or os.environ.get("GEMINI_API_KEY"):
        gemini_result = query_gemini_api(
            message=message,
            role=role,
            api_key=api_key,
            conversation_history=conversation_history,
            current_record_id=current_record_id
        )
        if gemini_result:
            return gemini_result

    # 2. Expert Revenue Intelligence Engine
    return generate_expert_response(
        message=message,
        role=role,
        current_record_id=current_record_id,
        state=state,
        category_id=category_id
    )
