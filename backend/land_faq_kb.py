"""
Comprehensive Land Records Knowledge Base (180+ Frequently Asked Questions)
Covers all 14 mandatory categories under Indian Land Revenue administration:
1. Land Ownership
2. Land Records (Khasra, Khata, Khatauni, Jamabandi, RoR, 7/12, Pahani, Fard)
3. Mutation (Dakhil-Kharij, Ferfar, Transfer)
4. Buying and Selling Land
5. Inheritance and Succession
6. Land Measurement and Boundaries (Conversions, Demarcation)
7. Land Disputes and Encroachment
8. Correction of Land Records (Name, Area, Survey No)
9. Government Land and Restrictions
10. Digital Land Records and Online Portals
11. Property Registration and Stamp Duty
12. Loans and Mortgages
13. Agricultural Land and Conversion
14. Citizen Help and Revenue Administration
"""
import re
from typing import List, Dict, Optional, Tuple, Any

FAQ_CATEGORIES = [
    {
        "id": "ownership",
        "name": "Land Ownership",
        "name_hi": "भूमि स्वामित्व",
        "icon": "user-check",
        "description": "Checking title, verifying legal ownership, joint tenures, and ownership certificates."
    },
    {
        "id": "records",
        "name": "Land Records",
        "name_hi": "भू-अभिलेख (खसरा/खतौनी/जमाबंदी)",
        "icon": "file-text",
        "description": "Understanding Khasra, Khata, Khatauni, Jamabandi, RoR, 7/12 Satbara, Pahani, and Fard."
    },
    {
        "id": "mutation",
        "name": "Mutation",
        "name_hi": "दाखिल-खारिज / नामांतरण",
        "icon": "refresh-cw",
        "description": "Procedure, documents, timelines, rejection reasons, and tracking for land mutation."
    },
    {
        "id": "buying_selling",
        "name": "Buying and Selling Land",
        "name_hi": "भूमि क्रय-विक्रय",
        "icon": "shopping-bag",
        "description": "Due diligence, title checks, sale deeds, encumbrance certificates, and seller verification."
    },
    {
        "id": "inheritance",
        "name": "Inheritance",
        "name_hi": "उत्तराधिकार एवं वसीयत",
        "icon": "users",
        "description": "Transfer of ancestral land after death, legal heir certificates, succession, and wills."
    },
    {
        "id": "measurement",
        "name": "Land Measurement and Boundaries",
        "name_hi": "पैमाइश, रकबा एवं सीमांकन",
        "icon": "compass",
        "description": "Acre, hectare, bigha, biswa, guntha, kanal conversions, plot boundaries, and ETS demarcation."
    },
    {
        "id": "disputes",
        "name": "Land Disputes",
        "name_hi": "भूमि विवाद एवं अतिक्रमण",
        "icon": "shield-alert",
        "description": "Illegal possession, boundary encroachments, revenue courts, SDM petitions, and remedies."
    },
    {
        "id": "correction",
        "name": "Correction of Land Records",
        "name_hi": "अभिलेख दुरुस्ती / संशोधन",
        "icon": "edit-3",
        "description": "Rectifying misspelled names, wrong area, incorrect parentage, or mistaken Khasra numbers."
    },
    {
        "id": "govt_land",
        "name": "Government Land and Restrictions",
        "name_hi": "सरकारी भूमि एवं प्रतिबंध",
        "icon": "landmark",
        "description": "Gram Sabha lands, forest zones, ceiling restrictions, public easements, and acquisition."
    },
    {
        "id": "digital_records",
        "name": "Digital Land Records",
        "name_hi": "डिजिटल भूलेख एवं ऑनलाइन सेवाएं",
        "icon": "globe",
        "description": "Bhulekh portals, digitally signed RoR downloads, QR code verification, and DigiLocker."
    },
    {
        "id": "registration",
        "name": "Property Registration",
        "name_hi": "संपत्ति पंजीकरण एवं स्टाम्प ड्यूटी",
        "icon": "award",
        "description": "Sub-Registrar Office (SRO) procedures, stamp duty rates, registration fees, and deed types."
    },
    {
        "id": "loans_mortgage",
        "name": "Loans and Mortgages",
        "name_hi": "बैंक ऋण, बंधक एवं भारमुक्त प्रमाणपत्र",
        "icon": "credit-card",
        "description": "KCC loans, title deeds for mortgage, non-encumbrance certificates (Form 15/16), and bank liens."
    },
    {
        "id": "agricultural",
        "name": "Agricultural Land",
        "name_hi": "कृषि भूमि एवं भू-उपयोग परिवर्तन",
        "icon": "sprout",
        "description": "Section 143/80 conversion (143/NA), ceiling laws, tenancy rights, and agricultural restrictions."
    },
    {
        "id": "citizen_help",
        "name": "Citizen Help",
        "name_hi": "नागरिक सहायता एवं राजस्व कार्यालय",
        "icon": "help-circle",
        "description": "Contacting Patwari, Tehsildar, Revenue Inspector, online grievances, RTI, and timelines."
    }
]

LAND_FAQ_DATABASE = [
    # =========================================================================
    # CATEGORY 1: LAND OWNERSHIP (13 FAQs)
    # =========================================================================
    {
        "id": "faq-own-01",
        "category": "Land Ownership",
        "category_id": "ownership",
        "question": "How can I check who owns a piece of land?",
        "question_hi": "जमीन का असली मालिक कौन है यह कैसे पता करें?",
        "answer": "To check land ownership in India:\n1. **Online State Portal**: Visit your state revenue portal (e.g. UP Bhulekh, MP Bhulekh, Mahabhulekh, Dharani, Bhoomi Karnataka) and select your District, Tehsil, and Village.\n2. **Search by Identifiers**: Search using the Khasra / Survey number, Khata number, or the owner's name.\n3. **Inspect the Record of Rights (RoR)**: The digital Khatauni / 7/12 extract will display the registered tenure holders, their father's name, their share, and any mortgage/lien remarks.\n4. **Sub-Registrar Search**: Check the Sub-Registrar Office (SRO) for registered sale deeds from the past 13 to 30 years to confirm legal chain of title.",
        "keywords": ["check land ownership", "find owner name", "who owns land", "malik ka naam", "asli malik", "owner search", "title check", "bhulekh search"],
        "state_notes": "Known as Khatauni in UP/Uttarakhand/Delhi, 7/12 Satbara in Maharashtra/Gujarat, RTC/Pahani in Karnataka, Dharani in Telangana, Jamabandi in Punjab/Haryana/Rajasthan.",
        "related_questions": ["How do I verify whether the seller is the real owner?", "What is the difference between Khata and Khasra number?", "How do I check if land is joint property?"]
    },
    {
        "id": "faq-own-02",
        "category": "Land Ownership",
        "category_id": "ownership",
        "question": "How do I verify whether the seller is the real owner before buying land?",
        "question_hi": "जमीन खरीदने से पहले विक्रेता के मालिकाना हक की जांच कैसे करें?",
        "answer": "Follow this 5-step seller verification checklist:\n1. **Check Latest Khatauni / RoR**: Verify that the seller's name appears as the current tenure holder in official revenue records, not just an old sale deed.\n2. **Inspect Chain of Title (Pattavali)**: Trace previous sale deeds for at least 30 years to confirm unbroken transfer of ownership.\n3. **Obtain Non-Encumbrance Certificate (EC / Form 15)**: Confirms that the seller has not already mortgaged, pledged, or sold the land to a third party.\n4. **Verify Physical Possession (Kabza)**: Visit the field in person to confirm that the seller actually possesses the land and there is no tenant or squatter dispute.\n5. **Check Identity & Aadhaar**: Cross-reference the seller's Aadhaar and PAN cards with the revenue record and registered deed details.",
        "keywords": ["verify seller", "real owner verification", "title verification", "fake seller", "original owner check", "dhokhadhadi se bache", "kabza check"],
        "state_notes": "In Maharashtra, verify Form 6 (Mutation extract) alongside 7/12. In Karnataka, check Form 9 and 11. In UP, check e-District registered deed status.",
        "related_questions": ["What is an Encumbrance Certificate?", "What documents are required to buy land?", "How do I know if land is mortgaged?"]
    },
    {
        "id": "faq-own-03",
        "category": "Land Ownership",
        "category_id": "ownership",
        "question": "What is joint ownership of land and how does it work?",
        "question_hi": "संयुक्त स्वामित्व (Joint Ownership) क्या होता है?",
        "answer": "Joint ownership occurs when two or more persons are registered as co-owners (Sah-Khatedar / Co-sharers) of the same parcel or Khata:\n- **Undivided Shares**: All co-owners have an undivided interest in every inch of the land until a legal partition (Batwara) is formally executed.\n- **Sale by Co-owner**: A single co-owner can legally sell ONLY their specified share percentage. They cannot sell a specific physical portion (e.g. front road-facing corner) without mutual consent or partition decree.\n- **Sum of Shares**: The sum of shares among all co-sharers in the government Khatauni must equal exactly 100% (or fraction 1.0).",
        "keywords": ["joint ownership", "co-sharer", "sah-khatedar", "shared land", "samyukta khata", "undivided share", "co-owner rights"],
        "state_notes": "Regulated under Section 116/117 of UP Revenue Code 2006; Section 85 of Maharashtra Land Revenue Code; and Section 44 of Transfer of Property Act.",
        "related_questions": ["How can co-owners divide their land legally?", "Can a co-owner sell land without consent of others?", "What happens if co-sharer shares do not total 100%?"]
    },
    {
        "id": "faq-own-04",
        "category": "Land Ownership",
        "category_id": "ownership",
        "question": "Can a co-owner sell their share of joint land without consent of other co-sharers?",
        "question_hi": "क्या कोई सह-खातेदार अन्य खातेदारों की सहमति के बिना अपना हिस्सा बेच सकता है?",
        "answer": "Under Section 44 of the Transfer of Property Act:\n1. A co-owner **can legally sell their undivided share** percentage without requiring written consent from other co-owners.\n2. However, the buyer acquires **only the undivided right**, NOT physical possession of any specific corner or road-facing side.\n3. The buyer must file a suit for partition under revenue law to get a distinct physically demarcated plot.\n4. **Right of Pre-emption**: In some states, other family co-sharers have a preferential right to purchase the share before it is sold to a stranger.",
        "keywords": ["co-owner sell share", "bina sahamati jameen bechna", "can co-sharer sell", "undivided share sale", "pre-emption right"],
        "state_notes": "In UP, Section 89 restricts sale of fragmented shares below 3.125 acres without permission under certain circumstances.",
        "related_questions": ["What is joint ownership of land?", "How can co-owners divide their land legally?", "What is an undivided share?"]
    },
    {
        "id": "faq-own-05",
        "category": "Land Ownership",
        "category_id": "ownership",
        "question": "What is an Ownership Certificate or Land Possession Certificate (LPC)?",
        "question_hi": "भूमि स्वामित्व प्रमाणपत्र या LPC क्या होता है?",
        "answer": "A Land Possession Certificate (LPC) or Ownership Certificate is an official certificate issued by the Revenue Department (Circle Officer / Tehsildar / Talukdar) confirming:\n- That you are the lawful, registered owner of the designated Khasra / Survey number.\n- That you are in actual, uninterrupted physical possession of the land.\n- It is frequently required for obtaining bank agricultural loans (KCC), government crop subsidies, tube-well connections, and bail bonds in court.",
        "keywords": ["ownership certificate", "land possession certificate", "lpc certificate", "dakhil kabza praman patra", "swamitva praman patra"],
        "state_notes": "Widely issued in Bihar, Jharkhand, UP, and West Bengal via state online revenue portals like Bihar Bhumi or e-District.",
        "related_questions": ["How can I check who owns a piece of land?", "What land documents are required for a bank loan?", "What is Record of Rights (RoR)?"]
    },
    {
        "id": "faq-own-06",
        "category": "Land Ownership",
        "category_id": "ownership",
        "question": "How is land ownership legally transferred from one person to another?",
        "question_hi": "जमीन का मालिकाना हक एक व्यक्ति से दूसरे व्यक्ति को कैसे ट्रांसफर होता है?",
        "answer": "Transfer of land ownership requires a mandatory two-step legal process in India:\n1. **Step 1: Execution & Registration of Deed**: A registered instrument (Sale Deed, Gift Deed, Relinquishment Deed, or Partition Deed) executed on non-judicial stamp paper at the Sub-Registrar Office (SRO) under the Registration Act 1908.\n2. **Step 2: Mutation (Dakhil-Kharij)**: Applying to the local Revenue Department (Tehsildar / Talathi / Patwari) to update the Record of Rights (Khatauni / 7/12 extract). Registration transfers title; mutation updates tax and revenue ownership.",
        "keywords": ["ownership transfer", "malikana hak transfer", "transfer land title", "sale deed to mutation", "how to transfer land"],
        "state_notes": "In Telangana (Dharani portal), deed registration and mutation happen simultaneously in a single integrated slot.",
        "related_questions": ["What is mutation and why is it important?", "What is the difference between registration and mutation?", "What documents are required to buy land?"]
    },
    {
        "id": "faq-own-07",
        "category": "Land Ownership",
        "category_id": "ownership",
        "question": "Does having a registered Sale Deed automatically make you the owner in government records?",
        "question_hi": "क्या रजिस्ट्री होने से अपने आप सरकारी रिकॉर्ड में नाम दर्ज हो जाता है?",
        "answer": "No. A registered Sale Deed proves legal title between buyer and seller, but **it does not automatically update the revenue Record of Rights (Khatauni / 7/12)**:\n- Until you apply for and obtain a **Mutation Order (दाखिल-खारिज / नामांतरण)**, the government records will continue showing the seller's name.\n- Without mutation, you cannot pay land revenue in your name, obtain bank crop loans, or prevent the seller from fraudulently claiming the land again.\n- Always apply for mutation immediately after registering a sale deed.",
        "keywords": ["registry vs mutation", "registry ho gayi naam nahi chadha", "sale deed vs khatauni", "is sale deed enough", "namantaran jaruri hai kya"],
        "state_notes": "Some states (like UP and MP) now trigger automated provisional mutation notices from SRO, but formal proclamation and verification remain mandatory.",
        "related_questions": ["What is mutation?", "How to apply for mutation after buying land?", "What happens if mutation is not done?"]
    },
    {
        "id": "faq-own-08",
        "category": "Land Ownership",
        "category_id": "ownership",
        "question": "What is adverse possession and can someone claim ownership by staying on my land?",
        "question_hi": "प्रतिकूल कब्जा (Adverse Possession) क्या है और क्या कोई मेरी जमीन पर कब्जा करके मालिक बन सकता है?",
        "answer": "Adverse possession is a legal doctrine under the Limitation Act 1963:\n- If an unauthorized person continuously, openly, and hostily occupies private land for **more than 12 years** without objection from the true owner, the true owner's legal right to file an eviction lawsuit expires.\n- For Government land, this limitation period is **30 years**.\n- However, the Supreme Court has ruled that mere permissive possession (e.g. tenant or caretaker) does NOT qualify as adverse possession. The possessor must prove hostile, uninterrupted animus possidendi.\n- If someone encroaches on your land, immediately lodge a police complaint and file an injunction / eviction suit before 12 years elapse.",
        "keywords": ["adverse possession", "pratikul kabza", "12 saal kabza", "squatter rights", "illegal occupant ownership", "limitation act 12 years"],
        "state_notes": "Governed by Article 65 of Limitation Act 1963 and relevant State Land Revenue Codes.",
        "related_questions": ["What to do if someone illegally occupies my land?", "How do I check if my land has encroachments?", "What is land demarcation?"]
    },
    {
        "id": "faq-own-09",
        "category": "Land Ownership",
        "category_id": "ownership",
        "question": "What is the difference between Freehold and Leasehold land ownership?",
        "question_hi": "फ्रीहोल्ड (Freehold) और लीजहोल्ड (Leasehold) जमीन में क्या अंतर है?",
        "answer": "- **Freehold Land**: You own the land and the structure perpetually without any time limit. You can sell, gift, mortgage, or transfer it freely without needing permission or paying ground rent to government development authorities.\n- **Leasehold Land**: You hold the right to occupy and use the land for a fixed duration (commonly 99 years) leased from a government authority (e.g. NOIDA, DDA, CIDCO, HUDA). Ownership remains with the authority, ground rent is payable, and conversion to freehold requires paying conversion charges and obtaining an NOC.",
        "keywords": ["freehold vs leasehold", "99 year lease", "freehold conversion", "noida leasehold", "patte par jameen", "ownership type"],
        "state_notes": "Development authority lands in NOIDA, Greater Noida, and parts of Delhi/Mumbai are primarily 99-year leasehold.",
        "related_questions": ["How is land ownership legally transferred?", "What documents are required to buy land?", "Can agricultural land be converted to freehold?"]
    },
    {
        "id": "faq-own-10",
        "category": "Land Ownership",
        "category_id": "ownership",
        "question": "Can an NRI (Non-Resident Indian) or OCI buy agricultural land in India?",
        "question_hi": "क्या कोई अनिवासी भारतीय (NRI/OCI) भारत में कृषि भूमि खरीद सकता है?",
        "answer": "Under FEMA (Foreign Exchange Management Act) regulations administered by the Reserve Bank of India (RBI):\n1. **NRIs and OCIs CANNOT buy agricultural land, plantation property, or farmhouses** in India.\n2. **Commercial & Residential Property**: NRIs/OCIs are fully permitted to buy residential and commercial properties.\n3. **Inheritance Exception**: An NRI/OCI can inherit agricultural land from an Indian resident parent or relative.\n4. Prior approval from the RBI is required if an NRI seeks to acquire agricultural land through any non-standard route.",
        "keywords": ["nri land purchase", "can nri buy agricultural land", "oci property buying", "fema land rules", "nri kheti ki jameen"],
        "state_notes": "Subject to Section 6(5) of FEMA 1999 and RBI Master Direction on Acquisition of Immovable Property in India.",
        "related_questions": ["What documents are required to buy land?", "Transfer of land after death of owner", "Restrictions on agricultural land"]
    },
    {
        "id": "faq-own-11",
        "category": "Land Ownership",
        "category_id": "ownership",
        "question": "What is female co-ownership or single female land rights under Hindu Succession Act?",
        "question_hi": "हिंदू उत्तराधिकार अधिनियम के तहत महिलाओं और बेटियों का जमीन में क्या अधिकार है?",
        "answer": "Under the Hindu Succession (Amendment) Act 2005 and Supreme Court ruling in *Vineeta Sharma v. Rakesh Sharma (2020)*:\n- Daughters have the **exact same coparcenary rights** in ancestral land by birth as sons.\n- A daughter remains a joint co-owner of ancestral land regardless of whether she is married or whether her father was alive on September 9, 2005.\n- A widow, mother, and daughters are Class-I legal heirs and inherit equal shares alongside sons when a male landowner dies intestate (without a will).\n- Their names can be added to Khatauni / Jamabandi through Varisatan / succession application.",
        "keywords": ["female land rights", "daughter property rights", "hindu succession act 2005", "betiyo ka jameen me hissa", "women land ownership"],
        "state_notes": "In UP, Section 108-110 of UP Revenue Code previously gave preference to male heirs, but constitutional amendments and court decrees uphold gender equality.",
        "related_questions": ["Transfer of land after death of owner", "Who are legal heirs for land inheritance?", "How can co-owners divide their land legally?"]
    },
    {
        "id": "faq-own-12",
        "category": "Land Ownership",
        "category_id": "ownership",
        "question": "What is the SVAMITVA Scheme and Property Card (Sampatti Card)?",
        "question_hi": "स्वामित्व (SVAMITVA) योजना और प्रॉपर्टी कार्ड क्या है?",
        "answer": "SVAMITVA (Survey of Villages and Mapping with Improvised Technology in Village Areas) is a central government initiative by the Ministry of Panchayati Raj:\n- It maps inhabited rural village areas (Abadi dehaat) using high-resolution Drones.\n- It provides rural villagers with a formal **Property Card (Sampatti Card / Gharauni)** certifying ownership of their residential houses in village abadi.\n- These cards allow villagers to use their residential homes as financial assets to take bank loans, clear property disputes, and pay gram panchayat taxes.",
        "keywords": ["svamitva scheme", "property card", "gharauni", "drone mapping village", "abadi land ownership", "sampatti card"],
        "state_notes": "Implemented across UP (called Gharauni), Maharashtra (Sanad / Property Card), Haryana (Lal Dora Free Property Certificate), and MP.",
        "related_questions": ["How can I check who owns a piece of land?", "What are land documents required for a bank loan?", "What is the difference between agricultural and residential land?"]
    },

    # =========================================================================
    # CATEGORY 2: LAND RECORDS (16 FAQs)
    # =========================================================================
    {
        "id": "faq-rec-01",
        "category": "Land Records",
        "category_id": "records",
        "question": "What are government land records?",
        "question_hi": "सरकारी भू-अभिलेख (Land Records) क्या होते हैं?",
        "answer": "Land records are official government registers maintained by the state Revenue Department that document:\n1. **Ownership & Title**: Names of registered landowners (Khatedar) and their share percentages.\n2. **Parcel Identifiers**: Khasra / Survey number, Khata number, and boundary map.\n3. **Area & Land Classification**: Total area (hectares, acres, bighas) and classification (agricultural, residential, barren, forest, government).\n4. **Encumbrances & Cultivation**: Details of bank mortgages, court stays, crop cultivation (Girdawari), and revenue tax payable.",
        "keywords": ["what are land records", "bhu abhilekh kya hai", "revenue records meaning", "land registry documents", "government records"],
        "state_notes": "Digitized under Digital India Land Records Modernization Programme (DILRMP).",
        "related_questions": ["What is a Khasra number?", "What is a Khata number?", "What is Khatauni?"]
    },
    {
        "id": "faq-rec-02",
        "category": "Land Records",
        "category_id": "records",
        "question": "What is a Khasra number (Survey number)?",
        "question_hi": "खसरा नंबर (Khasra / Survey Number) क्या होता है?",
        "answer": "A Khasra number (or Survey / Gut / Dag number) is a **unique identity number assigned to a specific geographical plot of land** in a village by the Revenue Department:\n- It acts like the Aadhaar number for a plot of land.\n- It identifies the plot's exact boundaries, physical shape on the village cadastral map (Shajra), area, soil type, and crops grown.\n- When a plot is subdivided among co-owners or sold in parts, sub-numbers are created (e.g. Khasra 105/1, 105/2).",
        "keywords": ["khasra number", "what is khasra", "survey number", "gut number", "dag number", "khasra kya hota hai", "plot identity"],
        "state_notes": "Termed 'Khasra' in UP, MP, Rajasthan, Punjab; 'Survey Number' or 'Gat Number' in Maharashtra; 'Survey Number' in Karnataka/Telangana; 'Dag Number' in Assam/WB.",
        "related_questions": ["What is a Khata number?", "What is Khatauni?", "How to find plot boundaries?"]
    },
    {
        "id": "faq-rec-03",
        "category": "Land Records",
        "category_id": "records",
        "question": "What is a Khata number and how is it different from a Khasra number?",
        "question_hi": "खाता नंबर (Khata Number) क्या होता है और यह खसरा नंबर से कैसे अलग है?",
        "answer": "- **Khata Number (Account Number)**: Identifies an entire family or set of co-owners who hold land together in a village. A single Khata number may contain multiple different Khasra plots owned by that same family.\n- **Khasra Number (Plot Number)**: Identifies a single, specific geographical piece of land on the ground.\n- **Key Difference**: Khata is the 'Account of Landowners', whereas Khasra is the 'Identity of the Physical Land Plot'. A landowner has one Khata number but can own 5 different Khasra plots listed under it.",
        "keywords": ["khata number", "difference between khata and khasra", "khata vs khasra", "khata kya hai", "account number land"],
        "state_notes": "Also called 'Khewat Number' in Punjab and Haryana; 'Khata' in UP, MP, and Bihar.",
        "related_questions": ["What is a Khasra number?", "What is Khatauni?", "What is Jamabandi?"]
    },
    {
        "id": "faq-rec-04",
        "category": "Land Records",
        "category_id": "records",
        "question": "What is Khatauni?",
        "question_hi": "खतौनी (Khatauni) क्या होती है?",
        "answer": "Khatauni is the primary **Register of Land Holdings (Record of Rights)** maintained by the Revenue Department:\n- It lists all the land owned by a person or family within a specific village, grouped by their Khata number.\n- It contains columns showing: Tenure holder name, Father/Husband name, Residence, List of all Khasra plots, Area of each plot, Revenue tax payable, and Remarks (which record bank mortgages, court stays, or mutation orders).\n- A certified copy of the Khatauni is standard legal proof of agricultural land holding.",
        "keywords": ["khatauni", "what is khatauni", "khatauni kya hoti hai", "ror extract", "record of rights khatauni", "up bhulekh khatauni"],
        "state_notes": "Prepared every 6 years in UP/Uttarakhand as 'Fasli Khatauni'. Equivalent to Jamabandi in Punjab/Haryana/Rajasthan.",
        "related_questions": ["What is a Khasra number?", "How to download land records online?", "How to check if land is mortgaged?"]
    },
    {
        "id": "faq-rec-05",
        "category": "Land Records",
        "category_id": "records",
        "question": "What is a 7/12 Extract (Satbara Utara)?",
        "question_hi": "7/12 (सातबारा उतारा) क्या होता है?",
        "answer": "The 7/12 Extract (Satbara Utara) is the official land register extract in Maharashtra and Gujarat under the Land Revenue Code:\n- **Village Form VII (Top section)**: Records rights, owner names, tenure category, survey/gut number, total area, and encumbrances/bank loans.\n- **Village Form XII (Bottom section)**: Records agricultural crop details (Pik-Pahani), fallow land, irrigation type, and trees.\n- It is accessed online via the **Mahabhulekh (Aaple Abhilekh)** portal.",
        "keywords": ["7 12 extract", "satbara utara", "7 12 kya hota hai", "mahabhulekh 7 12", "form 7 12", "pik pahani"],
        "state_notes": "Specific to Maharashtra and Gujarat. Form 8A provides Khata holding summary, Form 6 shows mutation history (Ferfar).",
        "related_questions": ["What is Ferfar (Form 6)?", "How to download land records online?", "What is Jamabandi?"]
    },
    {
        "id": "faq-rec-06",
        "category": "Land Records",
        "category_id": "records",
        "question": "What is Jamabandi?",
        "question_hi": "जमाबंदी (Jamabandi) क्या होती है?",
        "answer": "Jamabandi is the official **Record of Rights (RoR)** in northern Indian states like Punjab, Haryana, Rajasthan, Himachal Pradesh, and Jammu & Kashmir:\n- It is prepared once every 4 or 5 years by the Patwari.\n- It records details of ownership (Khewat), cultivation (Khatoni), parcel numbers (Khasra), area, share fraction, land revenue, and mortgage/lease encumbrances.\n- A certified extract of Jamabandi is commonly referred to as a **Fard**.",
        "keywords": ["jamabandi", "what is jamabandi", "jamabandi nakal", "punjab jamabandi", "haryana jamabandi", "fard jamabandi"],
        "state_notes": "Maintained online via portals like PLRS (Punjab), Jamabandi Haryana, and Apna Khata (Rajasthan).",
        "related_questions": ["What is Fard?", "What is a Khasra number?", "How to download land records online?"]
    },
    {
        "id": "faq-rec-07",
        "category": "Land Records",
        "category_id": "records",
        "question": "What is Fard?",
        "question_hi": "फर्द (Fard) क्या होता है?",
        "answer": "A 'Fard' is a certified printout or excerpt taken from the official Jamabandi or revenue register:\n- It acts as legal documentary proof of land ownership, area, and co-sharer status at a given point in time.\n- Commonly required by banks for Kisan Credit Card (KCC) loans, courts for bail bonds, and Sub-Registrars for sale deed registration in Punjab, Haryana, and Delhi.",
        "keywords": ["fard", "what is fard", "fard nakal", "fard nikalna", "land certificate fard"],
        "state_notes": "Common in Punjab, Haryana, Himachal, Delhi, and Western UP.",
        "related_questions": ["What is Jamabandi?", "What is Khatauni?", "What are land documents required for a bank loan?"]
    },
    {
        "id": "faq-rec-08",
        "category": "Land Records",
        "category_id": "records",
        "question": "What is Pahani / RTC in Southern States?",
        "question_hi": "पहाणी (Pahani) या RTC क्या होता है?",
        "answer": "In Karnataka, Andhra Pradesh, and Telangana, the **RTC (Record of Rights, Tenancy and Crops)** is colloquially known as **Pahani**:\n- It records: Landowner names and shares (Part A), Survey/Hissa number, Total extent and classification, Tenant or self-cultivation details (Part B), and Season-wise crops grown (Kharif/Rabi).\n- In Karnataka, it is downloaded from the **Bhoomi** portal. In Telangana, it is available on **Dharani**.",
        "keywords": ["pahani", "rtc pahani", "bhoomi rtc", "dharani pahani", "telangana pahani", "karnataka land records"],
        "state_notes": "Official equivalent of Khatauni/7-12 in Karnataka, AP, and Telangana.",
        "related_questions": ["What is Record of Rights (RoR)?", "How to download land records online?", "What is a Khasra number?"]
    },
    {
        "id": "faq-rec-09",
        "category": "Land Records",
        "category_id": "records",
        "question": "What is Record of Rights (RoR)?",
        "question_hi": "अभिलेख अधिकार (Record of Rights / RoR) क्या होता है?",
        "answer": "Record of Rights (RoR) is the universal legal statutory term under Indian Land Revenue Acts for the master register showing who holds rights in land:\n- It records legal title holders, co-tenants, mortgages, leases, government easements, and statutory land revenue rates.\n- Depending on the state, RoR is published under names like Khatauni (UP), Jamabandi (Punjab/Haryana/Rajasthan), 7/12 (Maharashtra), RTC (Karnataka), Pahani (Telangana/AP), or Khatian (West Bengal/Bihar).",
        "keywords": ["record of rights", "ror", "what is ror", "ror extract", "adhikar abhilekh"],
        "state_notes": "All State RoRs are linked to the national DILRMP central standard by the Government of India.",
        "related_questions": ["What is Khatauni?", "What is Jamabandi?", "What is a 7/12 Extract?"]
    },
    {
        "id": "faq-rec-10",
        "category": "Land Records",
        "category_id": "records",
        "question": "What is a Shajra (Cadastral Map / Naksha)?",
        "question_hi": "शजरा (Shajra / भू-नक्शा) क्या होता है?",
        "answer": "A Shajra (or Bhu-Naksha / Cadastral Map) is the **official, scaled geographical map of a village** showing the exact boundaries, shape, and position of every individual Khasra plot:\n- Shows boundaries, village roads, canals, wells, and boundary reference pillars (Sahadda/Tri-junctions).\n- Can be downloaded online via state **BhuNaksha** portals.\n- Used by revenue inspectors and surveyors during Section 24 demarcation surveys to verify whether on-ground field boundaries match official revenue dimensions.",
        "keywords": ["shajra", "cadastral map", "bhu naksha", "village map", "khasra map", "jameen ka naksha"],
        "state_notes": "Available online via NIC BhuNaksha portal in over 24 states.",
        "related_questions": ["How to find plot boundaries?", "What is land demarcation?", "What is a Khasra number?"]
    },
    {
        "id": "faq-rec-11",
        "category": "Land Records",
        "category_id": "records",
        "question": "What is Girdawari (Crop Survey)?",
        "question_hi": "गिरदावरी (Girdawari) क्या होती है?",
        "answer": "Girdawari is the seasonal crop inspection and field survey conducted by the Patwari twice a year (Kharif and Rabi seasons):\n- The Patwari visits every Khasra plot and records: crops grown, area cultivated, fallow land, and source of irrigation.\n- **Significance**: Critical for claiming PM-Kisan benefits, Minimum Support Price (MSP) grain procurement, crop loss compensation under PM Fasal Bima Yojana, and proving actual physical possession (Kabza) during ownership disputes.",
        "keywords": ["girdawari", "crop survey", "khasra girdawari", "fasal girdawari", "patwari girdawari"],
        "state_notes": "Called 'Pik-Pahani' in Maharashtra, 'E-Panta' in Andhra Pradesh, 'Khasra Girdawari' in North India.",
        "related_questions": ["What is a Khasra number?", "What is a 7/12 Extract?", "Where to contact the Patwari?"]
    },
    {
        "id": "faq-rec-12",
        "category": "Land Records",
        "category_id": "records",
        "question": "How can I download a certified digital land record copy online?",
        "question_hi": "ऑनलाइन प्रमाणित डिजिटल खतौनी / नकल कैसे डाउनलोड करें?",
        "answer": "To download an officially valid, digitally signed land record:\n1. **Open State Portal**: Go to your state Bhulekh portal (e.g. `upbhulekh.gov.in`, `mahabhulekh.maharashtra.gov.in`, `bhoomi.karnataka.gov.in`).\n2. **Choose Certified Extract**: Select 'Digitally Signed Khatauni / Certified 7/12' instead of ordinary view-only copy.\n3. **Select Jurisdiction**: Enter District, Tehsil, Pargana, and Village name.\n4. **Search Plot**: Enter Khasra, Khata number, or owner name.\n5. **Pay Fee & Download**: Pay the nominal government fee (usually ₹10 to ₹20) via netbanking/UPI to download a certified PDF with a digital cryptographic signature and QR code.",
        "keywords": ["download land records", "certified khatauni download", "digital 7 12 download", "ror pdf download", "bhulekh nakal print"],
        "state_notes": "Digitally signed copies with QR codes are legally valid under Section 65B of Indian Evidence Act and IT Act 2000.",
        "related_questions": ["How to verify digitally signed land records?", "What is QR code verification on land records?", "What is Khatauni?"]
    },
    {
        "id": "faq-rec-13",
        "category": "Land Records",
        "category_id": "records",
        "question": "How do I verify whether a printed digital land record is genuine or fake?",
        "question_hi": "डिजिटल खतौनी असली है या फर्जी इसकी जांच कैसे करें?",
        "answer": "To verify authenticity of a digital land record:\n1. **Scan the QR Code**: Scan the printed QR code using your smartphone camera. It will direct you to the official government revenue portal (`.gov.in` domain) showing the authentic live record.\n2. **Match Verification Code**: Every certified copy has a unique 16-digit Certificate / Verification ID printed on it. Enter this ID on your state portal's 'Verify Certificate' page.\n3. **Inspect Digital Signature**: Check for the cryptographic digital signature badge of the Tehsildar / District Revenue Officer.\n4. **Check Date of Issue**: Land records are dynamic. Ensure the extract was generated recently, as mortgages or transfers could have occurred after an older print date.",
        "keywords": ["verify digital land record", "fake khatauni check", "qr code verification land", "asli naqal check", "certificate verification"],
        "state_notes": "All state portals (UP, MP, Maharashtra, Karnataka, Telangana) have online verification portals.",
        "related_questions": ["What is QR code verification on land records?", "How can I check who owns a piece of land?", "What is an Encumbrance Certificate?"]
    },
    {
        "id": "faq-rec-14",
        "category": "Land Records",
        "category_id": "records",
        "question": "What is Khatian in Eastern States (Bihar, WB, Jharkhand, Odisha)?",
        "question_hi": "खतियान (Khatian) क्या होता है?",
        "answer": "In West Bengal, Bihar, Jharkhand, and Odisha, **Khatian** is the fundamental Record of Rights:\n- It details the history of title, class of tenant, Khasra/Plot numbers, boundaries, rent, and cess.\n- **CS Khatian**: Cadastral Survey (older colonial record).\n- **RS Khatian**: Revisional Survey Khatian.\n- **LR Khatian**: Land Reforms Khatian (the modern, governing land record in West Bengal maintained on Banglarbhumi).",
        "keywords": ["khatian", "lr khatian", "rs khatian", "banglarbhumi khatian", "bihar khatian", "what is khatian"],
        "state_notes": "Maintained on Banglarbhumi (WB) and Bihar Bhumi portals.",
        "related_questions": ["What is Record of Rights (RoR)?", "What is a Khasra number?", "How to download land records online?"]
    },
    {
        "id": "faq-rec-15",
        "category": "Land Records",
        "category_id": "records",
        "question": "What is a Plot Number and how does it relate to Khasra Number?",
        "question_hi": "प्लॉट नंबर और खसरा नंबर में क्या संबंध है?",
        "answer": "- In rural areas, the terms **Plot Number** and **Khasra Number** are often used interchangeably.\n- In urban or semi-urban plotted layouts approved by town planning authorities (e.g. BDA, DDA, JDA, Town Planning Schemes), a large rural agricultural Khasra plot is subdivided into smaller residential/commercial 'Plot Numbers' (e.g. Plot No. 42 in Khasra No. 105).\n- Always check which parent Khasra number your urban plot belongs to, as title search is conducted in the parent Khasra records.",
        "keywords": ["plot number", "khasra vs plot", "layout plot number", "residential plot khasra", "plot number meaning"],
        "state_notes": "In urban approved layouts, plot number is referenced alongside RERA registration.",
        "related_questions": ["What is a Khasra number?", "How to verify land before buying?", "What is agricultural-to-residential land conversion?"]
    },
    {
        "id": "faq-rec-16",
        "category": "Land Records",
        "category_id": "records",
        "question": "What is Fasli Year (फसली वर्ष) mentioned in land records?",
        "question_hi": "खतौनी में लिखा फसली वर्ष (Fasli Year) क्या होता है?",
        "answer": "The Fasli year is an agricultural calendar introduced during Emperor Akbar's era that remains the official accounting year for revenue records across North India:\n- **Fasli Year begins on July 1 and ends on June 30**.\n- To convert modern Gregorian year to Fasli year: **Subtract 592** (e.g. 2024 - 592 = 1432 Fasli).\n- Khatauni records are traditionally revised once every 6 Fasli years (known as Shala Khatauni).",
        "keywords": ["fasli year", "fasli varsh", "what is fasli year", "1430 fasli", "khatauni fasli year"],
        "state_notes": "Used officially in UP, Delhi, Rajasthan, MP, Telangana (Fasli year 1350 legacy records).",
        "related_questions": ["What is Khatauni?", "What is Girdawari?", "What are government land records?"]
    },

    # =========================================================================
    # CATEGORY 3: MUTATION (14 FAQs)
    # =========================================================================
    {
        "id": "faq-mut-01",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "What is land mutation (Dakhil-Kharij / Namantaran)?",
        "question_hi": "दाखिल-खारिज (Mutation) क्या होता है?",
        "answer": "Mutation (known as **Dakhil-Kharij** in North India, **Namantaran** in MP/Rajasthan, **Ferfar** in Maharashtra, and **Inteqal** in Punjab) is the formal administrative process of updating government land records:\n- It removes (Kharij) the previous owner's name and enters (Dakhil) the new owner's name in the state Record of Rights (Khatauni / 7/12).\n- **Purpose**: Establishes who is legally responsible for paying land revenue tax and publicly acknowledges the transfer of tenure rights.",
        "keywords": ["what is mutation", "dakhil kharij", "namantaran kya hai", "ferfar kya hai", "inteqal", "mutation meaning"],
        "state_notes": "Governed by Sections 34/35 of UP Revenue Code; Section 149 of Maharashtra Land Revenue Code; and relevant State Land Revenue Acts.",
        "related_questions": ["How do I apply for mutation?", "What documents are required for mutation?", "What happens if mutation is not done?"]
    },
    {
        "id": "faq-mut-02",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "How do I apply for land mutation after purchasing property?",
        "question_hi": "जमीन खरीदने के बाद दाखिल-खारिज के लिए ऑनलाइन आवेदन कैसे करें?",
        "answer": "To apply for mutation after purchase:\n1. **Apply Online**: Visit your state revenue department portal (e.g. UP e-District/Vaad portal, MP Bhulekh, MahaBhulekh Aaple Sarkar, Dharani, Bihar Bhumi).\n2. **Upload Required Documents**: Upload scanned registered sale deed, current Khatauni copy, and buyer/seller Aadhaar details.\n3. **Public Proclamation (Ishtehaar)**: The Naib Tehsildar court issues an automated public notice displayed at the Tehsil notice board and Gram Panchayat for 30–35 days to invite any third-party objections.\n4. **Patwari Inspection & Report**: The local Patwari submits a report confirming physical possession and absence of dispute.\n5. **Mutation Order**: If no objections are received, the Naib Tehsildar passes the Mutation Order (Aadesh) and updates the Khatauni.",
        "keywords": ["apply for mutation", "mutation process", "dakhil kharij online apply", "how to apply mutation", "mutation step by step"],
        "state_notes": "In Telangana (Dharani), registration and mutation occur simultaneously on the spot at the Sub-Registrar office.",
        "related_questions": ["What documents are required for mutation?", "What are reasons for mutation rejection?", "How to track mutation status?"]
    },
    {
        "id": "faq-mut-03",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "What documents are required for mutation of land?",
        "question_hi": "दाखिल-खारिज कराने के लिए कौन-कौन से दस्तावेज़ चाहिए?",
        "answer": "The standard document checklist for land mutation includes:\n1. **Certified Copy of Registered Deed** (Sale deed, Gift deed, or Partition deed).\n2. **Form 35 Application** (or state mutation application form).\n3. **Current Record of Rights (Khatauni / 7-12 / Jamabandi copy)**.\n4. **Identity Proof**: Aadhaar Card, PAN Card, and Voter ID of buyer and seller.\n5. **Affidavit**: Stating that the land holding does not breach state Land Ceiling Act limits and is free from court attachments.\n6. **Death Certificate & Legal Heir Certificate** (if applying for mutation after inheritance).\n7. **Latest Land Revenue Tax Receipt**.",
        "keywords": ["documents for mutation", "dakhil kharij documents", "mutation kagajat", "mutation checklist", "form 35 mutation"],
        "state_notes": "Check state-specific e-District portal for specific localized affidavit formats.",
        "related_questions": ["How do I apply for mutation?", "What is mutation after inheritance?", "Reasons for mutation rejection"]
    },
    {
        "id": "faq-mut-04",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "What is the statutory time limit for completing mutation under Citizen Charter?",
        "question_hi": "दाखिल-खारिज होने में कानूनी रूप से कितना समय लगता है?",
        "answer": "Under state Right to Public Services Acts (Citizen Charters):\n- **Uncontested Mutation (No objections)**: Standard processing time is **35 to 45 working days** from the date of filing the application.\n- **Contested Mutation (Objection filed)**: Converted into a contested revenue lawsuit before the Naib Tehsildar / Tehsildar court; statutory guideline is **90 days**, though complex disputes with evidence hearings may take longer.\n- If your undisputed application exceeds 45 days, you can file a First Appeal before the Tehsildar / SDM under the Public Services Guarantee Act.",
        "keywords": ["mutation time limit", "dakhil kharij kitne din me hota hai", "mutation processing time", "citizen charter mutation", "mutation delay"],
        "state_notes": "35 days in UP, 30 days in MP, 21 days in Haryana, immediate in Telangana Dharani.",
        "related_questions": ["How to track mutation status?", "Reasons for mutation rejection", "Where to file complaint if Patwari delays mutation?"]
    },
    {
        "id": "faq-mut-05",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "What are the common reasons for rejection of a mutation application?",
        "question_hi": "दाखिल-खारिज खारिज (Reject) होने के मुख्य कारण क्या हैं?",
        "answer": "A mutation application can be rejected due to:\n1. **Third-Party Objection (Aapatti)**: A co-sharer, family member, or previous buyer files an objection claiming adverse title or lack of partition.\n2. **Court Injunction / Stay Order**: An active stay order (Stay) issued by a Civil Court, Revenue Court, or High Court under Order 39 CPC.\n3. **Seller Had No Title / Defective Title**: The seller's name was not updated or their registered share was less than the area sold.\n4. **Ceiling Act Breach**: The purchase breaches state agricultural ceiling limits or tribal land transfer restrictions (Section 157-A in UP, Section 73AA in Maharashtra).\n5. **Government / Gram Sabha Land**: Plot overlaps with Gram Sabha pasture, pond, or road reserve.\n6. **Discrepancy in Deed vs Record**: Discrepancy between Khasra number or area stated in the Sale Deed vs the actual government Khatauni.",
        "keywords": ["mutation rejection reasons", "dakhil kharij kyu reject hota hai", "mutation objection", "stay on mutation", "rejection grounds"],
        "state_notes": "If rejected, an appeal lies before the Sub-Divisional Officer (SDO) / Deputy Collector within 30 days.",
        "related_questions": ["How to check if land is under dispute?", "What to do if mutation is rejected?", "How to correct mutation details?"]
    },
    {
        "id": "faq-mut-06",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "What should I do if my mutation application is rejected by the Tehsildar?",
        "question_hi": "यदि तहसीलदार द्वारा दाखिल-खारिज खारिज कर दिया जाए तो क्या करें?",
        "answer": "If your mutation application is rejected:\n1. **Obtain Certified Copy of Order**: Apply to the Revenue Court Copying Section (Nakal Vibhag) for a certified copy of the rejection order stating the exact legal grounds.\n2. **File an Appeal**: File a Statutory Appeal under Section 35(2) of the Revenue Code before the **Sub-Divisional Magistrate (SDM / SDO)** court within **30 days** from the date of the order.\n3. **Rectification Deed (if typographical error)**: If rejection occurred because of an incorrect Khasra number or spelling in the Sale Deed, execute a registered Rectification Deed (Tatima Registry) with the seller and re-apply.\n4. **Civil Title Suit**: If complex title ownership questions are disputed, file a declaratory title suit before the Civil Court.",
        "keywords": ["mutation rejected what to do", "appeal against mutation rejection", "sdm appeal mutation", "tatima registry", "dakhil kharij appeal"],
        "state_notes": "Appeal lies to SDO/Sub-Divisional Officer; Revision lies before Additional Commissioner; Final Revision before Board of Revenue.",
        "related_questions": ["Reasons for mutation rejection", "How to correct wrong survey or khasra number?", "Where to contact revenue department?"]
    },
    {
        "id": "faq-mut-07",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "What happens if I never do mutation after buying land?",
        "question_hi": "जमीन खरीदने के बाद यदि दाखिल-खारिज न कराया जाए तो क्या नुकसान होगा?",
        "answer": "Neglecting to complete mutation has severe legal and financial consequences:\n- **Government Record Shows Old Owner**: In the eyes of the government, the seller remains the registered owner.\n- **Risk of Fraudulent Resale**: Dishonest sellers can sell the land again to an unsuspecting second buyer or mortgage it to a bank, creating complex court litigation.\n- **Cannot Pay Land Tax**: You cannot pay revenue cess in your name or claim government disaster crop relief.\n- **No Bank Loans**: Banks will refuse to grant Kisan Credit Cards (KCC) or home construction loans without your name in the Khatauni.\n- **Government Acquisition Compensation**: If land is acquired by NHAI or railway, compensation is paid to the person listed in the Khatauni, not the unregistered deed holder.",
        "keywords": ["mutation na karane ke nuksan", "consequences of no mutation", "why mutation is necessary", "importance of dakhil kharij", "fraud without mutation"],
        "state_notes": "The Supreme Court in multiple rulings has held that while registration transfers title, mutation is indispensable for revenue recognition and public fiscal rights.",
        "related_questions": ["What is mutation?", "Does registered Sale Deed automatically make you owner?", "How to apply for mutation?"]
    },
    {
        "id": "faq-mut-08",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "What is mutation after inheritance (Varisatan / Virasat)?",
        "question_hi": "वारिसान (Virasat) या फौती नामांतरण क्या होता है?",
        "answer": "When a registered landowner dies, the process of transferring their land to their lawful heirs is called **Virasat / Varisatan / Fauti Namantaran**:\n- **Undisputed Succession**: Can be done through an online application on state revenue portals (e.g. UP e-District Varisatan, MP Fauti Namantaran).\n- **Patwari Inquiry**: The Patwari visits the village, confirms the date of death, prepares the family tree (Shajra Nasab / Parivar register extract), and lists all Class-I legal heirs (widow, sons, daughters, mother).\n- **Automated Order**: If no will is disputed, the Revenue Inspector / Tehsildar enters all heirs' names in the Khatauni with equal joint shares.",
        "keywords": ["varisatan", "virasat mutation", "fauti namantaran", "mutation after death", "inheritance mutation", "father death land transfer"],
        "state_notes": "In UP, Section 33 allows Patwari to register undisputed Virasat directly without court fee.",
        "related_questions": ["Transfer of land after death of owner", "Who are legal heirs for land inheritance?", "Will-related land transfer"]
    },
    {
        "id": "faq-mut-09",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "Can mutation be done based on an unregistered Will (Vasiyat)?",
        "question_hi": "क्या बिना रजिस्टर्ड वसीयत (Will) के आधार पर दाखिल-खारिज हो सकता है?",
        "answer": "Under Indian law:\n- An **unregistered will is legally valid** if executed properly with two attesting witnesses.\n- **However, in Revenue Courts**: If family co-heirs dispute the unregistered will, the Tehsildar cannot adjudicate the genuineness of the will. The Tehsildar will order standard statutory succession (Virasat) to all natural legal heirs and direct the will beneficiary to obtain a **Probate or Title Declaration decree from a competent Civil Court**.\n- A **registered will** carries stronger evidentiary presumption, but can still be challenged if other heirs claim coercion, fraud, or mental incapacity.",
        "keywords": ["mutation on will", "unregistered will dakhil kharij", "vasiyat par mutation", "probate of will", "will dispute land"],
        "state_notes": "Supreme Court held in *Suraj Lamp & Industries* that revenue authorities have summary jurisdiction and cannot determine complex testamentary validity.",
        "related_questions": ["What is mutation after inheritance?", "Will-related land transfer", "Who are legal heirs for land inheritance?"]
    },
    {
        "id": "faq-mut-10",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "How can I check the online status of my mutation application?",
        "question_hi": "दाखिल-खारिज की ऑनलाइन स्थिति (Status) कैसे चेक करें?",
        "answer": "To track your mutation status:\n1. Visit your state revenue portal (e.g., UP Vaad / e-District, MP Bhulekh, Bihar Bhumi, Mahabhulekh).\n2. Click on **'Mutation Application Status' (दाखिल-खारिज स्थिति)**.\n3. Search using your **Application Number / Case Number (वाद संख्या)**, Registration Deed Number, or Applicant Name.\n4. The tracking timeline will show current status: Notice Issued -> Patwari Report Submitted -> Objection Hearing -> Order Passed -> ROR Updated (Amal-Daramad).",
        "keywords": ["check mutation status", "track dakhil kharij", "mutation case status", "vaad status check", "online mutation tracking"],
        "state_notes": "Available 24/7 across UP Vaad portal, MP Saara/RCMS, Bihar Bhumi Dakhil Kharij status, Maharashtra Aaple Sarkar.",
        "related_questions": ["How do I apply for mutation?", "What is the statutory time limit for mutation?", "What are reasons for mutation rejection?"]
    },
    {
        "id": "faq-mut-11",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "What is Ferfar in Maharashtra Land Records?",
        "question_hi": "महाराष्ट्र में फेरफार (Ferfar / Form 6) क्या होता है?",
        "answer": "In Maharashtra, **Ferfar (Village Form 6 / Register of Mutations)** is the official register where every transaction affecting land ownership is first recorded:\n- When land is bought, inherited, partitioned, or mortgaged, the Talathi makes a provisional Ferfar entry.\n- A notice (Form 135-D) is served to all interested parties giving **15 days** to submit objections.\n- If no valid objection is filed, the Circle Officer certifies the Ferfar, and only then is the 7/12 Satbara extract updated.\n- You can download certified Ferfar extracts online via **Aaple Abhilekh** portal.",
        "keywords": ["ferfar", "form 6 ferfar", "what is ferfar", "mahabhulekh ferfar", "ferfar utara", "talathi ferfar"],
        "state_notes": "Regulated under Chapter X of Maharashtra Land Revenue Code 1966.",
        "related_questions": ["What is a 7/12 Extract?", "What is mutation?", "How to download land records online?"]
    },
    {
        "id": "faq-mut-12",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "What is Inteqal in Punjab and Haryana?",
        "question_hi": "पंजाब और हरियाणा में इंतकाल (Inteqal) क्या होता है?",
        "answer": "In Punjab, Haryana, and Himachal Pradesh, **Inteqal** is the official term for Mutation:\n- When a sale deed is registered, the Patwari enters an Inteqal in the mutation register.\n- The Tehsildar / Naib Tehsildar visits the village during a Jalsa-e-Aam (public gathering) to verify identity, check for objections, and formally sanction the Inteqal.\n- Once sanctioned, the Inteqal is incorporated into the next 4-yearly Jamabandi (RoR).",
        "keywords": ["inteqal", "what is inteqal", "punjab inteqal", "haryana inteqal", "inteqal verification", "inteqal register"],
        "state_notes": "Governed by Punjab Land Revenue Act 1887; accessible on PLRS and Jamabandi Haryana portals.",
        "related_questions": ["What is Jamabandi?", "What is Fard?", "What is mutation?"]
    },
    {
        "id": "faq-mut-13",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "What is Amal-Daramad (अमलदरामद) in land records?",
        "question_hi": "खतौनी में अमलदरामद (Amal-Daramad) का क्या अर्थ है?",
        "answer": "Amal-Daramad literally means **'implementation / physical entry'** in revenue terminology:\n- When a Tehsildar or Revenue Court passes an order (such as a mutation order, boundary demarcation decree, or court stay removal), the clerk or Patwari physically enters that order into Column 7 (Remarks/Tippani) of the Khatauni.\n- The process of writing that judicial order into the live ledger is called **Amal-Daramad**.\n- Until Amal-Daramad is executed, the order remains on paper but does not reflect in your printed online Khatauni extract.",
        "keywords": ["amal daramad", "khatauni amal daramad", "revenue court implementation", "what is amal daramad", "order entry khatauni"],
        "state_notes": "Standard Urdu/Persian revenue term used in UP, Uttarakhand, MP, Delhi, and Bihar.",
        "related_questions": ["What is Khatauni?", "What is mutation?", "How to track mutation status?"]
    },
    {
        "id": "faq-mut-14",
        "category": "Mutation",
        "category_id": "mutation",
        "question": "How do I correct an error made during the mutation process?",
        "question_hi": "दाखिल-खारिज में हुई लिपिकीय या नाम की गलती कैसे ठीक करें?",
        "answer": "If an error was made during mutation (such as a misspelled name, wrong share fraction, or omitted co-heir):\n1. **Clerical Error (Section 38 UP Revenue Code)**: File an application for correction of clerical / arithmetical mistake before the Tehsildar within the prescribed limitation period.\n2. **Recall Application**: If the mutation order was passed ex-parte (without serving notice to you), you can file an application to recall the order under revenue court rules.\n3. **Revision / Appeal**: File an appeal before the Sub-Divisional Officer (SDO) under Section 35(2) within 30 days of discovery of the error.",
        "keywords": ["correct mutation error", "dakhil kharij sudhar", "namantaran durusti", "recall mutation order", "clerical mistake in mutation"],
        "state_notes": "Governed by Section 38 of UP Revenue Code 2006; Section 155 of MLRC 1966.",
        "related_questions": ["What to do if mutation is rejected?", "How to correct wrong owner's name?", "What are reasons for mutation rejection?"]
    },

    # =========================================================================
    # CATEGORY 4: BUYING AND SELLING LAND (16 FAQs)
    # =========================================================================
    {
        "id": "faq-buy-01",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "What essential documents must I check before buying agricultural land?",
        "question_hi": "कृषि भूमि खरीदने से पहले कौन-कौन से मुख्य कागजात जांचने चाहिए?",
        "answer": "Before paying an advance or token money, examine these essential documents:\n1. **Latest Certified Khatauni / 7-12 / RoR**: Check seller's name, ownership share, and total area.\n2. **Original Registered Title Deeds (Chain of Title)**: Prior deeds for the past 30 years.\n3. **Nil-Encumbrance Certificate (EC / Form 15)**: Proof that the land has no prior mortgage or court attachment.\n4. **Village Shajra (Cadastral Map)**: Check plot shape and ensure access road exists.\n5. **Latest Land Tax Receipt (Malguzari / Lagan)**.\n6. **No-Dues Certificate (NOC)** from the local Primary Agricultural Cooperative Society (PACS) or bank.\n7. **Identity Verification**: Seller's Aadhaar and PAN cards.",
        "keywords": ["documents before buying land", "land buying checklist", "jameen kharidne se pehle kagajat", "title search checklist", "due diligence land"],
        "state_notes": "In Maharashtra, verify 7/12, 8A, and Form 6 Ferfar. In Karnataka, check RTC, Mutation register extract, and Form 9/11.",
        "related_questions": ["How do I verify whether the seller is the real owner?", "What is an Encumbrance Certificate?", "How to check if land is under dispute?"]
    },
    {
        "id": "faq-buy-02",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "What is an Encumbrance Certificate (EC) and why is it mandatory?",
        "question_hi": "भारमुक्त प्रमाणपत्र (Encumbrance Certificate / EC) क्या है?",
        "answer": "An Encumbrance Certificate (EC / भारमुक्त प्रमाण पत्र) is an official document issued by the Sub-Registrar Office (SRO):\n- **Purpose**: Certifies whether any registered transactions, mortgages, charges, court attachments, or liens exist against the property over a requested period (commonly 12 to 30 years).\n- **Form 15**: Issued if encumbrances/mortgages or sales are found, detailing the registered instruments.\n- **Form 16 (Nil-Encumbrance)**: Issued if no registered mortgages, liens, or charges exist during the specified search period. A Nil-EC is mandatory for bank home/land loans.",
        "keywords": ["encumbrance certificate", "what is ec", "nil encumbrance certificate", "form 15 form 16", "bharmukta praman patra", "ec certificate online"],
        "state_notes": "Available online via state registration portals like Kaveri (Karnataka), IGR Maharashtra, Meeseva (Telangana), and e-District (UP).",
        "related_questions": ["What is Form 15 and Form 16?", "What land documents are required for a bank loan?", "How to verify seller before buying?"]
    },
    {
        "id": "faq-buy-03",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "What is the difference between an Agreement to Sell and a Sale Deed?",
        "question_hi": "एग्रीमेंट टू सेल (Agreement to Sell) और सेल डीड (Sale Deed) में क्या अंतर है?",
        "answer": "- **Agreement to Sell (बिक्री एकरारनामा)**: A contract promising to transfer property in the future upon satisfaction of agreed terms (such as full payment, boundary demarcation, or bank loan approval). **It does NOT transfer ownership or title.**\n- **Sale Deed (बैनामा / विक्रय विलेख)**: The final legal document executed and registered at the Sub-Registrar Office on stamp paper. **It immediately conveys absolute ownership title** from seller to buyer under Section 54 of Transfer of Property Act.",
        "keywords": ["agreement to sell vs sale deed", "bainama vs ikrarnama", "difference agreement and sale deed", "registry vs agreement", "stamp paper agreement"],
        "state_notes": "Supreme Court in *Suraj Lamp & Industries (2012)* reaffirmed that immovable property can only be transferred through a registered Sale Deed.",
        "related_questions": ["How property registration works?", "What is Stamp Duty and Registration Charge?", "Documents required for property registration"]
    },
    {
        "id": "faq-buy-04",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "How do I check whether a piece of land has an ongoing court dispute?",
        "question_hi": "जमीन पर कोई कोर्ट केस या विवाद तो नहीं चल रहा यह कैसे पता करें?",
        "answer": "To check for court disputes and *lis pendens*:\n1. **Check Khatauni / 7-12 Remarks Column**: Revenue court stay orders, attachment notices, or Section 24 demarcation applications are recorded in the remarks column.\n2. **State Revenue Court Management System**: Search by Khasra number on your state's online revenue court portal (e.g. UP Vaad `vaad.up.nic.in`, MP Saara/RCMS, Bihar Revenue Court).\n3. **e-Courts Services Portal (`ecourts.gov.in`)**: Search District Civil Courts by village name, party name, or survey number.\n4. **Public Notice in Local Newspapers**: Publish a 15-day public title notice in two local newspapers through an advocate inviting any third-party claims or objections before executing the deed.",
        "keywords": ["check land court case", "dispute check", "court stay on land", "lis pendens", "jameen par court case", "vaad portal search"],
        "state_notes": "Search online via `ecourts.gov.in` and respective State Revenue Court portals.",
        "related_questions": ["What is a land dispute?", "What is an Encumbrance Certificate?", "How to verify seller before buying?"]
    },
    {
        "id": "faq-buy-05",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "What is Stamp Duty and Registration Fee when buying land?",
        "question_hi": "जमीन की रजिस्ट्री में स्टाम्प ड्यूटी और रजिस्ट्रेशन फीस क्या होती है?",
        "answer": "- **Stamp Duty**: A state government tax levied under the Indian Stamp Act 1899 on the conveyance of immovable property. It usually ranges between **4% to 7%** of the property's Circle Rate or market value, whichever is higher.\n- **Registration Fee**: An administrative charge (typically **1%** of the property value, often capped) paid to the Sub-Registrar Office for registering and archiving the deed.\n- **Concessions**: Most states offer a **1% to 2% stamp duty discount** if the property is registered in the name of a female buyer.",
        "keywords": ["stamp duty", "registration charges", "registry kharcha", "stamp duty calculation", "circle rate stamp duty", "female stamp duty concession"],
        "state_notes": "Stamp duty varies by state: UP (7% male, 6% female), Maharashtra (5%-6% + 1% Metro cess), Karnataka (5%), Delhi (6% male, 4% female).",
        "related_questions": ["What is Circle Rate / Ready Reckoner Rate?", "How property registration works?", "What documents are required to buy land?"]
    },
    {
        "id": "faq-buy-06",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "What is Circle Rate (Ready Reckoner Rate / Guidance Value)?",
        "question_hi": "सर्कल रेट (Circle Rate / Ready Reckoner Rate) क्या होता है?",
        "answer": "The Circle Rate (also called **Ready Reckoner Rate** in Maharashtra or **Guidance Value** in Karnataka/Tamil Nadu) is the **minimum benchmark price per square meter / acre** set by the District Magistrate below which land cannot be registered:\n- **Taxes Calculated on Circle Rate**: Even if you purchase a plot for ₹10 Lakhs, if the government circle rate evaluates it at ₹15 Lakhs, you must pay stamp duty on ₹15 Lakhs.\n- **Income Tax Section 56(2)(x)**: Selling significantly below circle rate triggers income tax penalties on both buyer and seller.\n- Circle rate tables are updated annually and published on district administration websites.",
        "keywords": ["circle rate", "ready reckoner rate", "guidance value", "circle rate kya hai", "minimum registration rate", "dm circle rate"],
        "state_notes": "Known as Circle Rate in North India, Ready Reckoner Rate in Maharashtra, Guidance Value in Karnataka/TN, Minimum Value in AP/Telangana.",
        "related_questions": ["What is Stamp Duty and Registration Fee?", "How property registration works?", "What is an Agreement to Sell?"]
    },
    {
        "id": "faq-buy-07",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "Can I buy agricultural land if I am not a farmer (Non-Agriculturist)?",
        "question_hi": "क्या कोई गैर-किसान (Non-Agriculturist) कृषि भूमि खरीद सकता है?",
        "answer": "Rules vary strictly by state:\n- **States where Non-Farmers CANNOT buy agricultural land**: Maharashtra, Karnataka (partially relaxed), Gujarat, Himachal Pradesh (Sec 118 permission mandatory), Uttarakhand (hill districts capped at 250 sqm).\n- **States where ANY Indian citizen can buy agricultural land**: Uttar Pradesh, Madhya Pradesh, Haryana, Punjab, Rajasthan, Bihar, and West Bengal (subject to state land ceiling limits).\n- In restricted states, purchasing agricultural land without farmer status or government permission under Section 89/118 results in confiscation by the government.",
        "keywords": ["can non-farmer buy agricultural land", "non agriculturist buy farm land", "kisan na hone par jameen kharidna", "section 118 himachal", "farmer status land"],
        "state_notes": "Section 63/64 Bombay Tenancy Act (Maharashtra/Gujarat); Section 118 HP Tenancy Act; Section 79A/B Karnataka Land Reforms (amended 2020).",
        "related_questions": ["What is agricultural-to-residential land conversion?", "What documents are required to buy land?", "Restrictions on agricultural land"]
    },
    {
        "id": "faq-buy-08",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "Can land belonging to Scheduled Caste (SC) or Scheduled Tribe (ST) be purchased?",
        "question_hi": "क्या अनुसूचित जाति (SC) या अनुसूचित जनजाति (ST) की जमीन खरीदी जा सकती है?",
        "answer": "Land ownership of SC/ST tenure holders is protected by strict statutory safeguards to prevent exploitation:\n1. **SC Land Transfer**: An SC owner can only sell agricultural land to a non-SC buyer after obtaining **prior written permission from the District Magistrate (DM / Collector)**.\n2. **Retention Criterion**: Permission is granted only if the seller retains a statutory minimum agricultural holding (e.g., at least 3.125 acres in UP) after the sale.\n3. **ST Land Prohibition**: In most scheduled tribal areas, sale of ST land to non-ST persons is **strictly prohibited by law**.\n4. Any deed executed without the Collector's prior permission is void *ab initio*, and the land vests in the State Government.",
        "keywords": ["buy sc st land", "section 157 a up revenue code", "collector permission sc land", "dalit jameen kharidna", "tribal land transfer restriction"],
        "state_notes": "Section 98/99 of UP Revenue Code 2006; Section 73AA of MLRC 1966; Chhota Nagpur Tenancy (CNT) Act in Jharkhand.",
        "related_questions": ["What are reasons for mutation rejection?", "What documents are required to buy land?", "Government land and restrictions"]
    },
    {
        "id": "faq-buy-09",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "What is a 30-Year Search Report (Title Search Report)?",
        "question_hi": "30 साल की टाइटल सर्च रिपोर्ट (Title Search Report) क्या होती है?",
        "answer": "A Title Search Report is a formal legal evaluation conducted by an advocate or legal title investigator examining SRO records and revenue ledgers for the past **30 years**:\n- Traces all ownership mutations, sale deeds, gift deeds, partitions, and mortgages across three decades.\n- Verifies that the chain of title is clean, unbroken, and free from undisclosed co-sharers or minors' claims.\n- Mandatory for all commercial bank mortgage loans, real estate developers, and large land acquisitions.",
        "keywords": ["title search report", "30 year search", "title deed investigation", "advocate search report", "clean title proof"],
        "state_notes": "Standard national legal requirement under Transfer of Property Act 1882 for proving marketable title.",
        "related_questions": ["What is an Encumbrance Certificate?", "How do I verify whether the seller is the real owner?", "What land documents are required for a bank loan?"]
    },
    {
        "id": "faq-buy-10",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "What precautions should I take when buying land from a Power of Attorney (PoA) holder?",
        "question_hi": "पावर ऑफ अटॉर्नी (PoA) धारक से जमीन खरीदते समय क्या सावधानियां बरतनी चाहिए?",
        "answer": "Buying land through a General Power of Attorney (GPA) carries high risk. Follow these precautions:\n1. **Registered PoA Only**: The PoA must be registered at the Sub-Registrar Office. An unregistered or notarized PoA is invalid for sale of property.\n2. **Specific Power to Sell**: Ensure the PoA explicitly grants the power to sell and receive consideration money.\n3. **Principal Must Be Alive**: A PoA automatically becomes null and void the moment the original owner dies or revokes it.\n4. **Direct Confirmation**: Speak directly with the original owner to confirm that the PoA has not been cancelled or revoked.\n5. **Payment in Owner's Name**: Ensure payment is made by cheque/RTGS directly into the bank account of the original owner, not the attorney.",
        "keywords": ["power of attorney land", "poa property purchase", "gpa sale risk", "mukhtarnama", "buying from attorney"],
        "state_notes": "Supreme Court in *Suraj Lamp (2012)* ruled that GPA sales do not convey legal title without a registered Sale Deed.",
        "related_questions": ["What is the difference between an Agreement to Sell and a Sale Deed?", "How property registration works?", "How to verify seller before buying?"]
    },
    {
        "id": "faq-buy-11",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "What is a Mutation Order and why should I ask the seller for it?",
        "question_hi": "विक्रेता से दाखिल-खारिज आदेश (Mutation Order) की प्रति क्यों मांगनी चाहिए?",
        "answer": "A Mutation Order is the judicial decree passed by the Tehsildar approving entry of the seller's name into the government Khatauni:\n- Asking for the seller's original mutation order proves how the seller acquired the land (by purchase, partition, or inheritance).\n- It confirms that the previous owner's name was officially removed without pending objections.\n- Never purchase land based solely on an unmutated sale deed.",
        "keywords": ["seller mutation order", "dakhil kharij aadesh", "namantaran aadesh copy", "verify mutation before buying"],
        "state_notes": "Available from the Tehsildar record room or online e-Court revenue portals.",
        "related_questions": ["What is mutation?", "Does registered Sale Deed automatically make you owner?", "What documents are required to buy land?"]
    },
    {
        "id": "faq-buy-12",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "What is TDS on property purchase (Section 194-IA) and who pays it?",
        "question_hi": "जमीन या प्रॉपर्टी खरीदने पर 1% TDS (Section 194-IA) कब कटता है?",
        "answer": "Under Section 194-IA of the Income Tax Act:\n- If the total sale consideration of immovable property (other than rural agricultural land) is **₹50 Lakhs or more**, the **buyer must deduct 1% TDS** from the payment to the seller.\n- The buyer must deposit this 1% TDS with the Income Tax Department using **Form 26QB** within 30 days and provide Form 16B certificate to the seller.\n- **Exemption**: Pure rural agricultural land (situated beyond municipal limits) is exempt from 1% TDS.",
        "keywords": ["tds on property", "section 194 ia", "1 percent tds land", "form 26qb", "tds agricultural land exemption"],
        "state_notes": "Rural agricultural land defined under Section 2(14)(iii) of the Income Tax Act 1961 is exempt.",
        "related_questions": ["What is Stamp Duty and Registration Fee?", "What documents are required to buy land?", "How property registration works?"]
    },
    {
        "id": "faq-buy-13",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "What is land demarcation (Hadbandi) and why should I get it done before buying?",
        "question_hi": "जमीन खरीदने से पहले हदबंदी या सीमांकन (Demarcation) क्यों कराना चाहिए?",
        "answer": "Land demarcation (Seemankan / Hadbandi) is the on-ground electronic survey conducted by the Revenue Inspector and Patwari using the official village map (Shajra):\n- **Prevents Buying Disputed Land**: Confirms that the boundaries on the ground match the area stated in the title deed.\n- **Uncovers Encroachments**: Detects whether neighbors have encroached on the boundaries or if a road/canal cuts through the plot.\n- Avoid purchasing land purely based on oral boundary descriptions without physical demarcation.",
        "keywords": ["demarcation before buying", "hadbandi before purchase", "boundary check", "plot physical measurement", "prevent encroachment purchase"],
        "state_notes": "Can be applied for under Section 24 of UP Revenue Code 2006 or Section 85 of MLRC 1966.",
        "related_questions": ["What is land demarcation?", "How to find plot boundaries?", "What to do when boundaries are incorrect?"]
    },
    {
        "id": "faq-buy-14",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "What is an agricultural land ceiling limit and can I buy unlimited farmland?",
        "question_hi": "कृषि भूमि सीलिंग कानून क्या है और क्या कोई असीमित जमीन खरीद सकता है?",
        "answer": "No. Under the **Agricultural Land Ceiling Acts** enacted across all Indian states:\n- There is a maximum ceiling on the total acreage of agricultural land an individual or family unit can own.\n- **Uttar Pradesh**: Maximum ceiling is **12.5 acres** (5.05 hectares) of irrigated land per family.\n- **Maharashtra**: 18 acres of perennially irrigated land, up to 54 acres of dry land.\n- **Penalty**: Any purchase exceeding the ceiling limit is declared surplus and vests automatically in the State Government without compensation.",
        "keywords": ["land ceiling limit", "maximum agricultural land allowed", "ceiling act up", "jameen ki adhiktam seema", "surplus land"],
        "state_notes": "UP Imposition of Ceiling on Land Holdings Act 1960; Maharashtra Agricultural Lands (Ceiling on Holdings) Act 1961.",
        "related_questions": ["Can a non-farmer buy agricultural land?", "What documents are required to buy land?", "Government land and restrictions"]
    },
    {
        "id": "faq-buy-15",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "What is a Public Notice (Jahir Prakatan) in newspapers before buying land?",
        "question_hi": "जमीन खरीदने से पहले अखबार में सार्वजनिक सूचना (Public Notice) क्यों दी जाती है?",
        "answer": "A Public Notice is an announcement published by your advocate in two local newspapers (one regional language and one English):\n- Discloses the intent of the buyer to purchase the designated Khasra / Survey number.\n- Invites any person holding a claim, mortgage, inheritance right, agreement, or court dispute to submit written objections within 14 or 15 days with documentary proof.\n- **Legal Benefit**: Proves that the buyer acted as a 'bona-fide purchaser for value without notice' under Section 3 of the Transfer of Property Act, shielding the transaction in future litigation.",
        "keywords": ["public notice land", "jahir prakatan", "newspaper notice property", "bona fide purchaser", "advocate public notice"],
        "state_notes": "Standard practice in Maharashtra, Gujarat, Karnataka, and major commercial transactions pan-India.",
        "related_questions": ["How do I verify whether the seller is the real owner?", "What is a 30-Year Search Report?", "How to check if land is under dispute?"]
    },
    {
        "id": "faq-buy-16",
        "category": "Buying and Selling Land",
        "category_id": "buying_selling",
        "question": "What are the risks of purchasing unapproved or unauthorized colony plots?",
        "question_hi": "अवैध या अनधिकृत कॉलोनी में प्लॉट खरीदने के क्या खतरे हैं?",
        "answer": "Buying unapproved residential plots carved out of agricultural land carries serious legal risks:\n1. **Demolition by Development Authority**: Authorities like DDA, BDA, GMDA, or LDA can demolish unapproved structures without compensation.\n2. **No Registry / Mutation**: Registrars may refuse to register sub-divided plots below minimum fragmented size, and municipal corporations will not issue building approval.\n3. **No Basic Infrastructure**: No legal road access, sewer lines, water supply, or electricity meters.\n4. **Section 143 Violation**: If the land was not legally converted from agricultural to non-agricultural status, the layout is illegal.\n- **Remedy**: Always verify RERA approval and Town Planning layout sanction before buying.",
        "keywords": ["unauthorized colony plot", "illegal plotting risk", "rera approved plot", "demolition risk land", "panchayat layout plot"],
        "state_notes": "Regulated under State Urban Planning Acts and Real Estate (Regulation and Development) Act (RERA) 2016.",
        "related_questions": ["What is agricultural-to-residential land conversion?", "What is Circle Rate?", "What documents are required to buy land?"]
    },

    # =========================================================================
    # CATEGORY 5: INHERITANCE (13 FAQs)
    # =========================================================================
    {
        "id": "faq-inh-01",
        "category": "Inheritance",
        "category_id": "inheritance",
        "question": "How is land transferred after the death of the registered owner?",
        "question_hi": "जमीन मालिक की मृत्यु के बाद जमीन वारिसों के नाम कैसे होती है?",
        "answer": "When a landowner dies:\n1. **Obtain Death Certificate**: From the local municipal office or Gram Panchayat.\n2. **Obtain Legal Heir Certificate / Family Register Extract**: Issued by the Tehsildar / SDO / Panchayat Officer listing all surviving lawful heirs.\n3. **Apply for Virasat / Varisatan Mutation**: Submit an application on the state revenue portal (e.g. UP e-District, MP Saara, Mahabhulekh).\n4. **Patwari Verification**: The Patwari visits the village, confirms the family tree (Shajra Nasab), and submits a report.\n5. **Revenue Order**: The Revenue Officer orders entry of all legal heirs' names into the Khatauni with equal undivided shares.",
        "keywords": ["transfer land after death", "inheritance land transfer", "virasat process", "father expired land transfer", "varisatan online"],
        "state_notes": "Governed by Section 33 of UP Revenue Code 2006; Section 149/150 of MLRC; Hindu Succession Act 1956.",
        "related_questions": ["Who are legal heirs for land inheritance?", "Can daughters claim share in ancestral land?", "What is mutation after inheritance?"]
    },
    {
        "id": "faq-inh-02",
        "category": "Inheritance",
        "category_id": "inheritance",
        "question": "Who are the legal heirs entitled to inherit agricultural land?",
        "question_hi": "कृषि भूमि के कानूनी वारिस कौन-कौन होते हैं?",
        "answer": "Under the Hindu Succession Act (applicable to Hindus, Sikhs, Jains, Buddhists):\n- **Class-I Legal Heirs** inherit equally:\n  1. Sons\n  2. Daughters (married or unmarried)\n  3. Surviving Widow\n  4. Mother of the deceased\n  5. Children of any pre-deceased son or daughter\n- If no Class-I heirs exist, property passes to Class-II heirs (father, siblings, grandchildren).\n- For Muslims, inheritance is governed by Muslim Personal Law (Shariat) where heirs receive designated Quranic fractional shares.",
        "keywords": ["legal heirs land", "who inherits land", "class 1 legal heirs", "kanuni waris", "family inheritance rights"],
        "state_notes": "State tenancy laws that previously favored sons have been harmonized with the Hindu Succession (Amendment) Act 2005.",
        "related_questions": ["Can daughters claim share in ancestral land?", "How is land transferred after the death of owner?", "What is a Legal Heir Certificate?"]
    },
    {
        "id": "faq-inh-03",
        "category": "Inheritance",
        "category_id": "inheritance",
        "question": "Do married daughters have an equal share in ancestral land?",
        "question_hi": "क्या विवाहित बेटियों का भी पैतृक जमीन में बराबर का हिस्सा होता है?",
        "answer": "Yes. Under the **Hindu Succession (Amendment) Act 2005** and the Supreme Court landmark judgment in *Vineeta Sharma v. Rakesh Sharma (2020)*:\n- Daughters are **coparceners by birth**, possessing the exact same rights and liabilities as sons.\n- **Marital status is irrelevant**: A daughter does not lose her right to ancestral property upon marriage.\n- It does not matter whether the father was alive or deceased on September 9, 2005.\n- If brothers refuse to include a sister's name in Virasat, she can file an objection before the Tehsildar or a partition suit in Revenue/Civil Court.",
        "keywords": ["married daughter land share", "daughter ancestral property", "betiyo ka jameen me adhikar", "supreme court daughter rights", "hindu succession 2005", "daughter inherit agricultural land", "can daughters inherit land", "daughters share in agricultural land", "beti ka hissa zameen me"],
        "state_notes": "Supreme Court *Vineeta Sharma (2020)* judgment binds all Indian states and overrides contradictory state revenue provisions.",
        "related_questions": ["Who are legal heirs for land inheritance?", "What is mutation after inheritance?", "How can co-owners divide their land legally?"]
    },
    {
        "id": "faq-inh-04",
        "category": "Inheritance",
        "category_id": "inheritance",
        "question": "What is a Succession Certificate and when is it required for land?",
        "question_hi": "उत्तराधिकार प्रमाणपत्र (Succession Certificate) क्या है और क्या यह जमीन के लिए चाहिए?",
        "answer": "- A **Succession Certificate** is issued by a Civil District Court under the Indian Succession Act 1925 primarily for movable assets (bank accounts, shares, mutual funds, provident fund).\n- For **Immovable Land/Property**: A Succession Certificate is generally NOT issued for land. Instead, revenue authorities require:\n  1. **Legal Heir Certificate / Waris Certificate** issued by the Tehsildar or SDO, OR\n  2. A **Letter of Administration / Declaratory Decree** from a Civil Court in contested inheritance disputes.",
        "keywords": ["succession certificate", "uttaradhikar praman patra", "legal heir vs succession certificate", "civil court succession"],
        "state_notes": "Revenue authorities accept Tehsildar Legal Heir Certificate for Khatauni mutation.",
        "related_questions": ["How is land transferred after the death of owner?", "Who are legal heirs for land inheritance?", "What is a Legal Heir Certificate?"]
    },
    {
        "id": "faq-inh-05",
        "category": "Inheritance",
        "category_id": "inheritance",
        "question": "What is a Relinquishment Deed (Hak Tyag Patra) in family inheritance?",
        "question_hi": "हक त्याग पत्र (Relinquishment Deed) क्या होता है?",
        "answer": "A Relinquishment Deed (Release Deed / Hak-Tyag / हक-त्याग पत्र) is a registered legal instrument through which one legal heir voluntarily surrenders their inherited share in favor of other co-heirs (e.g., sisters releasing their share to brothers, or a mother releasing to children):\n- **Must Be Registered**: Must be executed on non-judicial stamp paper and registered at the Sub-Registrar Office (SRO).\n- **Irrevocable**: Once registered, the relinquishing party cannot arbitrarily cancel it or claim the land back later.\n- Many states offer a highly concessional stamp duty (e.g. ₹500 to ₹1,000) for registered release deeds between blood relatives.",
        "keywords": ["relinquishment deed", "hak tyag patra", "release deed family", "surrender share land", "behan ka hissa tyagna"],
        "state_notes": "Stamp duty is nominal for blood relatives in UP, Maharashtra, Rajasthan, and MP.",
        "related_questions": ["Can daughters claim share in ancestral land?", "How is land transferred after the death of owner?", "How property registration works?"]
    },
    {
        "id": "faq-inh-06",
        "category": "Inheritance",
        "category_id": "inheritance",
        "question": "What happens if a landowner dies without leaving a Will (Intestate)?",
        "question_hi": "यदि जमीन मालिक बिना वसीयत लिखे मर जाए तो जमीन का क्या होता है?",
        "answer": "When a person dies without making a Will, it is termed **Intestate Succession**:\n1. The land is distributed strictly according to statutory personal law (e.g., Hindu Succession Act 1956 or Muslim Personal Law).\n2. All Class-I legal heirs (surviving spouse, mother, and all sons and daughters) become joint co-owners with **equal undivided shares**.\n3. The Patwari cannot exclude any legal heir without a registered relinquishment deed or court order.\n4. Any heir can subsequently file a suit for partition under Section 116 to demarcate their individual plot.",
        "keywords": ["die without will", "intestate succession", "bina vasiyat ke maut", "automatic inheritance", "equal share heirs"],
        "state_notes": "Statutory succession is recorded automatically under Section 33 of UP Revenue Code upon filing Virasat.",
        "related_questions": ["Who are legal heirs for land inheritance?", "How is land transferred after the death of owner?", "How can co-owners divide their land legally?"]
    },
    {
        "id": "faq-inh-07",
        "category": "Inheritance",
        "category_id": "inheritance",
        "question": "Can an inherited ancestral property be given away by Will to only one child?",
        "question_hi": "क्या पैतृक जमीन की वसीयत किसी एक बच्चे के नाम की जा सकती है?",
        "answer": "- **Ancestral Property (पैतृक संपत्ति)**: A person holds only their individual undivided share in ancestral coparcenary property. They **cannot will away the entire ancestral property** to one child, because other children have an independent birthright in it. They can only bequeath their own undivided share fraction.\n- **Self-Acquired Property (स्व-अर्जित संपत्ति)**: If the land was purchased by the father with his own earned funds, he has absolute right to will it to anyone he chooses (even one child or an outsider), completely excluding other heirs.",
        "keywords": ["will ancestral property", "can father will ancestral land", "paitrik sampatti vasiyat", "self acquired vs ancestral will"],
        "state_notes": "Under Hindu Law, coparcenary ancestral property cannot be completely alienated by will to deprive other coparceners of their birthright.",
        "related_questions": ["What is mutation based on a Will?", "Who are legal heirs for land inheritance?", "Can daughters claim share in ancestral land?"]
    },
    {
        "id": "faq-inh-08",
        "category": "Inheritance",
        "category_id": "inheritance",
        "question": "What is the difference between Ancestral Property and Self-Acquired Property?",
        "question_hi": "पैतृक संपत्ति और स्व-अर्जित संपत्ति में क्या अंतर है?",
        "answer": "- **Ancestral Property (पैतृक संपत्ति)**: Property inherited up to four generations of male lineage (father, grandfather, great-grandfather) that has remained undivided. Children acquire an **equal ownership share by birth**.\n- **Self-Acquired Property (स्व-अर्जित संपत्ति)**: Land purchased by an individual using their own income, or received via a gift deed or personal will. The owner has **100% exclusive control** to sell, gift, or bequeath it without needing permission from children or relatives.",
        "keywords": ["ancestral vs self acquired", "paitrik vs swa-arjit", "birthright in property", "can father sell ancestral land"],
        "state_notes": "Governed by Hindu Succession Act 1956 and principles of Mitakshara coparcenary law.",
        "related_questions": ["Can an inherited ancestral property be given away by Will?", "Can a father sell ancestral property without children's consent?", "Who are legal heirs for land inheritance?"]
    },
    {
        "id": "faq-inh-09",
        "category": "Inheritance",
        "category_id": "inheritance",
        "question": "Can a father sell ancestral land without the consent of his sons and daughters?",
        "question_hi": "क्या पिता बच्चों की सहमति के बिना पैतृक जमीन बेच सकता है?",
        "answer": "Under Hindu Law, a father (acting as Karta) can sell ancestral property without coparcener children's consent **ONLY under exceptional conditions**:\n1. **Legal Necessity (विधिक आवश्यकता)**: Family medical emergencies, marriage of daughters, or essential family sustenance.\n2. **Benefit of the Estate (हितार्थ)**: To preserve or defend family assets.\n3. **Indispensable Duties**: Performance of essential religious or funeral rites.\n- If a father sells ancestral property for frivolous reasons, personal vices, or gambling without legal necessity, the children can file a civil suit for cancellation of the sale deed and partition.",
        "keywords": ["can father sell ancestral land", "bina bacho ki sahamati paitrik jameen", "karta powers sale", "legal necessity property sale"],
        "state_notes": "Supreme Court rulings establish that the burden of proving 'legal necessity' rests upon the purchaser.",
        "related_questions": ["What is the difference between Ancestral Property and Self-Acquired Property?", "How can co-owners divide their land legally?", "Can daughters claim share in ancestral land?"]
    },
    {
        "id": "faq-inh-10",
        "category": "Inheritance",
        "category_id": "inheritance",
        "question": "What is Family Partition (Aapasi Batwara) of inherited land?",
        "question_hi": "पैतृक जमीन का आपसी पारिवारिक बंटवारा कैसे होता है?",
        "answer": "When multiple family members jointly inherit land, they can partition it via two routes:\n1. **Mutual Compromise Partition (आपसी सहमति बंटवारा)**: Co-sharers demarcate specific physical plots (Kurras) on the village map, execute a registered Partition Deed (Section 117 UP Revenue Code), and submit it to the Tehsildar for issuing separate Khata numbers.\n2. **Revenue Court Partition Suit (धारा 116 वाद)**: If brothers/co-owners cannot agree mutually, any co-owner can file a Suit for Division of Holding before the Sub-Divisional Officer (SDO). The court issues a preliminary decree determining shares, directs the Revenue Inspector to draw plot boundaries (Qurrabandi), and passes a final decree granting distinct Khasra numbers (e.g. 105/1, 105/2).",
        "keywords": ["family partition", "batwara process", "aapasi batwara", "section 116 partition", "qurrabandi", "divide ancestral land"],
        "state_notes": "Section 116/117 of UP Revenue Code 2006; Section 85 of MLRC 1966; Section 54 of Civil Procedure Code (CPC).",
        "related_questions": ["How can co-owners divide their land legally?", "What happens if co-sharer shares do not total 100%?", "What is land demarcation?"]
    },
    {
        "id": "faq-inh-11",
        "category": "Inheritance",
        "category_id": "inheritance",
        "question": "Can a step-mother or adopted child inherit agricultural land?",
        "question_hi": "क्या सौतेली मां या दत्तक (गोद लिया) बच्चा जमीन में वारिस हो सकता है?",
        "answer": "- **Adopted Child**: Under the Hindu Adoptions and Maintenance Act 1956, a legally adopted child has the **exact same legal inheritance rights** as a biological child in the adoptive parents' property.\n- **Step-Child**: A step-child has no automatic right in the step-parent's property unless legally adopted.\n- **Step-Mother**: A step-mother is not a Class-I legal heir of her step-son; she inherits as a widow in her deceased husband's property alongside his children.",
        "keywords": ["adopted child inheritance", "god liya bacha jameen", "step child property rights", "step mother land claim"],
        "state_notes": "Governed by Hindu Adoptions and Maintenance Act 1956 and Section 8 of Hindu Succession Act 1956.",
        "related_questions": ["Who are legal heirs for land inheritance?", "Transfer of land after death of owner", "What is an undivided share?"]
    },
    {
        "id": "faq-inh-12",
        "category": "Inheritance",
        "category_id": "inheritance",
        "question": "What is a Legal Heir Certificate and how can I obtain it?",
        "question_hi": "कानूनी वारिस प्रमाणपत्र (Legal Heir Certificate) कैसे बनता है?",
        "answer": "A Legal Heir Certificate (Warisana Praman Patra) is an official document establishing the living legal heirs of a deceased person:\n1. Apply online via your state e-District portal or submit an application to the Tehsildar / Talukdar.\n2. Submit: Death certificate, ration card, Parivar register extract, applicant Aadhaar, and an affidavit listing all family members and relationships.\n3. The Halka Patwari and Revenue Inspector conduct a spot verification in the village.\n4. Upon verification, the Tehsildar issues the certificate within **15 to 30 days**.",
        "keywords": ["legal heir certificate", "warisan certificate", "how to get legal heir certificate", "e-district legal heir", "family tree certificate"],
        "state_notes": "Issued via e-District portals in UP, Tamil Nadu, Karnataka, Andhra Pradesh, and Maharashtra.",
        "related_questions": ["How is land transferred after the death of owner?", "Who are legal heirs for land inheritance?", "What is mutation after inheritance?"]
    },

    # =========================================================================
    # CATEGORY 6: LAND MEASUREMENT AND BOUNDARIES (14 FAQs)
    # =========================================================================
    {
        "id": "faq-mea-01",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "How is land measured in India and what are standard units?",
        "question_hi": "भारत में जमीन की पैमाइश किन इकाइयों (Units) में होती है?",
        "answer": "Land is measured in metric and traditional units in India:\n- **Standard Metric Units**: Square Meters (m²), Hectares (ha).\n- **Standard Imperial Units**: Square Feet (sq ft), Square Yards (Gaj), Acres.\n- **Traditional State Units**: Bigha, Biswa, Guntha, Kanal, Marla, Cent, Ground, Katha.\n- **Crucial Rule**: While local land is discussed in Bighas or Gunthas, all official government Record of Rights (Khatauni) record area strictly in **Hectares** (with 4 decimal precision).",
        "keywords": ["land measurement units", "jameen ki paimayish", "acre hectare bigha conversion", "standard land units india", "how to measure land"],
        "state_notes": "1 Hectare = 10,000 m² = 2.471 Acres across all Indian states.",
        "related_questions": ["How many Bighas are in an Acre or Hectare?", "How do I convert square meters to acres?", "What is land demarcation?"]
    },
    {
        "id": "faq-mea-02",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "How many Bighas are in an Acre and Hectare?",
        "question_hi": "एक एकड़ और हेक्टेयर में कितने बीघे होते हैं?",
        "answer": "Because Bigha sizes vary by state and district:\n- **Uttar Pradesh (Standard Pucca Bigha)**:\n  - 1 Hectare = **3.95 Bigha**\n  - 1 Acre = **1.60 Bigha**\n  - 1 Bigha = 20 Biswa = 2,529.3 m² = 27,225 sq ft = 3,025 sq yards (Gaj).\n- **Rajasthan**:\n  - 1 Pucca Bigha = 27,225 sq ft (1 Acre = 1.6 Bigha).\n  - 1 Kaccha Bigha = 17,424 sq ft.\n- **Bihar & West Bengal**:\n  - 1 Bigha = 20 Katha = 14,400 sq ft (1 Acre = 3.025 Bighas).\n- **Always verify the local Gatha / Jarib measurement** used in your village's settlement record.",
        "keywords": ["how many bigha in acre", "bigha to hectare", "1 bigha kitna hota hai", "pucca bigha vs kaccha bigha", "bigha conversion"],
        "state_notes": "UP/Haryana: 1 Pucca Bigha = 3,025 Gaj. MP: 1 Bigha = 1,333.33 m².",
        "related_questions": ["How do I convert square meters to acres?", "What is Guntha in Maharashtra?", "What is Kanal and Marla?"]
    },
    {
        "id": "faq-mea-03",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "What is the formula to convert Square Meters to Hectares, Acres, and Square Yards?",
        "question_hi": "वर्ग मीटर को हेक्टेयर, एकड़ और वर्ग गज में बदलने का क्या फार्मूला है?",
        "answer": "Use these exact mathematical conversions:\n1. **Square Meters to Hectares**: Divide by 10,000\n   - Example: 2,400 m² ÷ 10,000 = **0.2400 Hectares**.\n2. **Square Meters to Acres**: Divide by 4,046.86 (or multiply by 0.0002471)\n   - Example: 2,400 m² ÷ 4,046.86 = **0.593 Acres**.\n3. **Square Meters to Square Yards (Gaj)**: Multiply by 1.19599\n   - Example: 100 m² = **119.6 sq yards (Gaj)**.\n4. **Square Meters to Square Feet**: Multiply by 10.7639\n   - Example: 100 m² = **1,076.4 sq ft**.",
        "keywords": ["sq meter to acre", "convert sq meter to hectare", "sq meter to sq yard", "gaj me badle", "land area conversion formula"],
        "state_notes": "Central government DILRMP standardizes all cadastral boundary polygons in WGS84 square meters.",
        "related_questions": ["How is land measured in India?", "How many Bighas are in an Acre or Hectare?", "What is a Khasra number?"]
    },
    {
        "id": "faq-mea-04",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "What is Guntha in Maharashtra and Karnataka?",
        "question_hi": "गुंठा (Guntha) क्या होता है?",
        "answer": "In Maharashtra, Karnataka, Gujarat, and Andhra Pradesh, land is commonly measured in **Gunthas**:\n- **1 Guntha = 1,089 Square Feet = 121 Square Yards (Gaj) = 101.17 Square Meters**.\n- **40 Gunthas = 1 Acre**.\n- **1 Hectare = Approximately 98.84 Gunthas (approx 100 Gunthas)**.\n- For example, an agricultural parcel of 2 Acres and 15 Gunthas equals 95 Gunthas total.",
        "keywords": ["guntha", "what is guntha", "1 guntha square feet", "guntha to acre", "maharashtra guntha calculation"],
        "state_notes": "Standard real estate and agricultural unit across Western and Southern India.",
        "related_questions": ["What is a 7/12 Extract?", "How is land measured in India?", "What is land demarcation?"]
    },
    {
        "id": "faq-mea-05",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "What is Kanal and Marla in Punjab, Haryana, and J&K?",
        "question_hi": "कनाल (Kanal) और मरला (Marla) क्या होता है?",
        "answer": "In Punjab, Haryana, Himachal Pradesh, and Jammu & Kashmir:\n- **1 Marla = 9 Sarsahi = 272.25 Square Feet = 25.29 Square Meters**.\n- **20 Marlas = 1 Kanal = 5,445 Square Feet = 505.85 Square Meters**.\n- **8 Kanals = 1 Acre (Killa / Ghumaon) = 160 Marlas = 43,560 sq ft**.\n- In urban residential plotting (e.g. Chandigarh, Mohali, Gurgaon), plots are frequently described as '1 Kanal' (approx 500 sq yards) or '10 Marla' (approx 250 sq yards).",
        "keywords": ["kanal and marla", "what is kanal", "what is marla", "1 kanal in sq yards", "punjab land measurement"],
        "state_notes": "Standard unit in Punjab, Haryana, J&K, and Pakistan Punjab.",
        "related_questions": ["What is Jamabandi?", "What is Fard?", "How is land measured in India?"]
    },
    {
        "id": "faq-mea-06",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "What is land demarcation (Seemankan / Hadbandi)?",
        "question_hi": "सीमांकन (Seemankan) या हदबंदी क्या होती है?",
        "answer": "Land demarcation is the official physical field survey conducted by revenue authorities to establish exact plot boundaries on the ground:\n- **Governing Law**: Section 24 of UP Revenue Code 2006; Section 85 of Maharashtra Land Revenue Code.\n- **Executing Officer**: Revenue Inspector (RI) and Halka Patwari using Electronic Total Station (ETS) / DGPS or metric measurement chains (Gunter's Chain / Jarib).\n- **Process**: Identifies permanent village reference points (Sahadda), matches the field with the village map (Shajra), sets fixed boundary stones (Simana Patthar), and draws up an official Panchnama.",
        "keywords": ["land demarcation", "seemankan", "hadbandi", "what is demarcation", "paimayish", "boundary measurement"],
        "state_notes": "Application filed in Form RC-22 before Tehsildar / SDM court.",
        "related_questions": ["How do I apply for Section 24 demarcation?", "What to do when boundaries are incorrect?", "How to resolve boundary encroachment?"]
    },
    {
        "id": "faq-mea-07",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "How do I apply for official boundary demarcation (Section 24 Seemankan)?",
        "question_hi": "धारा 24 के तहत सीमांकन (Seemankan) के लिए आवेदन कैसे करें?",
        "answer": "To get official revenue demarcation:\n1. **File Petition**: Submit an application under **Section 24** before the Sub-Divisional Magistrate (SDM) / Tehsildar court.\n2. **Deposit Treasury Fee**: Pay the government challan fee (standard: ₹1,000 per boundary pillar) via Cyber Treasury.\n3. **Notice to Adjoining Owners**: The SDM court issues a 15-day prior notice (Parwana) to adjoining plot owners informing them of the inspection date.\n4. **Spot Survey**: Revenue Inspector and Patwari conduct electronic ETS survey in presence of both parties and village panchas.\n5. **Demarcation Order**: If boundary pillars were broken or moved, the Tehsildar orders installation of boundary stones and eviction of encroachers within 30 days.",
        "keywords": ["apply for demarcation", "section 24 seemankan", "hadbandi online apply", "fee for demarcation", "sdm seemankan"],
        "state_notes": "Section 24 of UP Revenue Code 2006; Rule 22 of UP Revenue Code Rules 2016.",
        "related_questions": ["What is land demarcation?", "What to do when boundaries are incorrect?", "How to resolve boundary encroachment?"]
    },
    {
        "id": "faq-mea-08",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "What is an Electronic Total Station (ETS) / DGPS land survey?",
        "question_hi": "इलेक्ट्रॉनिक टोटल स्टेशन (ETS) या DGPS सर्वे क्या होता है?",
        "answer": "An Electronic Total Station (ETS) or Differential GPS (DGPS) survey is a modern satellite/laser-assisted land measurement technology:\n- Replaces manual iron chain (Jarib) measuring which was prone to sag, stretching, and human bias.\n- Measures slope distances, horizontal angles, and precise spatial coordinates with millimeter accuracy.\n- Coordinates are directly matched against georeferenced satellite village cadastral maps (GIS shapefiles).\n- The survey produces a tamper-proof digital boundary polygon ensuring zero boundary dispute ambiguity.",
        "keywords": ["ets survey", "electronic total station", "dgps land survey", "modern land measurement", "laser survey land"],
        "state_notes": "Mandated under DILRMP for modern cadastral resurveys across all Indian states.",
        "related_questions": ["What is land demarcation?", "How to find plot boundaries?", "What to do when boundaries are incorrect?"]
    },
    {
        "id": "faq-mea-09",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "What should I do if my neighbor has moved the boundary (Mendh) into my field?",
        "question_hi": "यदि पड़ोसी ने मेड़ काटकर मेरी जमीन दबा ली है तो क्या करें?",
        "answer": "If a neighbor cuts or shifts the boundary (Mendh/Dhur):\n1. **Do Not Engage in Physical Violence**: Take photos/videos of the altered boundary.\n2. **File Section 24 Demarcation Application**: Apply to the SDM / Tehsildar for urgent field demarcation.\n3. **Revenue Panchnama**: The Revenue Inspector inspects the field, verifies against Shajra map, and documents the exact encroachment area in square meters.\n4. **Restoration Order (Section 24(2))**: The Tehsildar directs the encroacher to restore the original boundary line within 30 days.\n5. **Police Enforcement**: If the neighbor resists or rebuilds the encroachment, the SDM requisitions police assistance to physically fix cement boundary pillars.",
        "keywords": ["neighbor moved boundary", "medh todna", "medh vivad", "encroachment by neighbor", "boundary displacement"],
        "state_notes": "UP Revenue Code Section 24; Section 138/139 of MLRC; Section 145 CrPC if breach of peace is imminent.",
        "related_questions": ["What is land demarcation?", "How do I apply for Section 24 demarcation?", "How to resolve boundary encroachment?"]
    },
    {
        "id": "faq-mea-10",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "What is a Jarib (Gunter's Chain) and how is it used in village surveys?",
        "question_hi": "जरीब (Jarib / Gunter Chain) क्या होती है?",
        "answer": "A Jarib is a traditional measuring chain made of 100 iron links used by Patwaris since the Mughal and British revenue settlements:\n- **Gunter's Jarib**: Length is **66 feet (20.12 meters = 4 rods = 22 yards)**.\n- **Shahjahani Jarib**: Length is 165 feet (used in parts of Western UP/Rajasthan).\n- 1 Acre is historically defined as an area of 10 square chains (66 ft × 660 ft).\n- Modern revenue departments are phasing out Jaribs in favor of laser ETS and DGPS instruments.",
        "keywords": ["jarib", "gunters chain", "patwari jarib", "iron chain measurement", "traditional land measurement"],
        "state_notes": "Still referenced in legacy village settlement records (Bandobast).",
        "related_questions": ["How is land measured in India?", "What is an Electronic Total Station (ETS) survey?", "What is a Khasra number?"]
    },
    {
        "id": "faq-mea-11",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "What is Sahadda (Tri-junction Pillar) in land demarcation?",
        "question_hi": "सहद्दा या सीहद्दा (Tri-junction Pillar) क्या होता है?",
        "answer": "A Sahadda (or Sihadda / Tri-junction pillar) is a **permanent stone or masonry monument erected at the meeting point of three village boundaries**:\n- It acts as the absolute, immutable reference benchmark for all village land surveys.\n- During any boundary dispute survey, the Revenue Inspector must tie the survey line back to the nearest intact Sahadda stone.\n- Damaging or removing a Sahadda stone is a punishable criminal offense under the Indian Penal Code and State Revenue Codes.",
        "keywords": ["sahadda", "sihadda", "tri junction pillar", "boundary pillar", "survey benchmark stone"],
        "state_notes": "Preserved under Section 227 of UP Revenue Code and Section 134 of MLRC.",
        "related_questions": ["What is land demarcation?", "How do I apply for Section 24 demarcation?", "What to do when boundaries are incorrect?"]
    },
    {
        "id": "faq-mea-12",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "What is Cent and Ground in South Indian land measurement?",
        "question_hi": "दक्षिण भारत में सेंट (Cent) और ग्राउंड (Ground) क्या होता है?",
        "answer": "In Tamil Nadu, Kerala, Andhra Pradesh, and parts of Karnataka:\n- **1 Cent = 435.6 Square Feet = 40.46 Square Meters = 48.4 Square Yards**.\n- **100 Cents = 1 Acre**.\n- **1 Ground (Tamil Nadu)** = **2,400 Square Feet = 222.96 Square Meters = 5.51 Cents**.\n- In urban residential areas in Chennai, plots are almost exclusively bought and sold in 'Grounds' (e.g. 1.5 grounds = 3,600 sq ft).",
        "keywords": ["cent to sq ft", "ground to sq ft", "tamil nadu land measurement", "1 cent kitna hota hai", "kerala cent measurement"],
        "state_notes": "Standard unit in Tamil Nadu, Kerala, AP, and Telangana.",
        "related_questions": ["How is land measured in India?", "What is Guntha in Maharashtra?", "How do I convert square meters to acres?"]
    },
    {
        "id": "faq-mea-13",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "What to do if on-ground area is smaller than the area mentioned in my Sale Deed?",
        "question_hi": "यदि जमीन का मौके पर रकबा रजिस्ट्री में लिखे रकबे से कम निकले तो क्या करें?",
        "answer": "If actual on-ground measurement reveals a shortfall in area:\n1. **Official Demarcation (Sec 24)**: First get an official demarcation to verify whether adjoining neighbors have encroached on your boundaries.\n2. **Check Village Shajra (Map)**: If the village map itself shows a smaller plot than your sale deed, the seller sold you non-existent excess land.\n3. **Recovery from Seller**: You can file a civil suit against the seller under Section 55 of Transfer of Property Act for partial refund of consideration money due to breach of title warranty.\n4. **Revenue Map Durusti**: If the error was a cartographic mapping mistake during village consolidation (Chakbandi), file a Map Correction suit under Section 30 of UP Revenue Code.",
        "keywords": ["area less on ground", "rakba kam nikalna", "shortfall in plot area", "sale deed area mismatch ground", "jameen kam nikalna"],
        "state_notes": "Map correction governed by Section 30 of UP Revenue Code 2006 or Section 106 of MLRC.",
        "related_questions": ["What is land demarcation?", "How to correct wrong land area in revenue records?", "How to resolve boundary encroachment?"]
    },
    {
        "id": "faq-mea-14",
        "category": "Land Measurement and Boundaries",
        "category_id": "measurement",
        "question": "What is Chakbandi (Consolidation of Land Holdings)?",
        "question_hi": "चकबंदी (Chakbandi / Consolidation) क्या होती है?",
        "answer": "Chakbandi (Consolidation) is a government land reform process whereby scattered, fragmented small agricultural parcels owned by a farmer across a village are consolidated into **one or two compact, large, rectangular plots (Chaks)**:\n- **Benefits**: Ensures direct access to a dedicated village farm road (Chak Road), irrigation channel (Chak Nali), and eliminates field boundary disputes.\n- **New Records Created**: During Chakbandi, the village undergoes complete resurvey, old Khasra numbers are replaced with new C.H. Form 41/45 numbers, and a revised Shajra map is published.\n- While Chakbandi is active in a village, ordinary civil court suits concerning title are abated.",
        "keywords": ["chakbandi", "consolidation of land", "chak road", "ch form 41", "chakbandi process", "fragmentation consolidation"],
        "state_notes": "Governed by UP Consolidation of Holdings Act 1953; Bombay Prevention of Fragmentation and Consolidation of Holdings Act 1947.",
        "related_questions": ["What is a Khasra number?", "What is a Shajra?", "What to do when boundaries are incorrect?"]
    },

    # =========================================================================
    # CATEGORY 7: LAND DISPUTES (14 FAQs)
    # =========================================================================
    {
        "id": "faq-disp-01",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "What are the common types of land disputes in India?",
        "question_hi": "भारत में भूमि विवाद के प्रमुख प्रकार कौन-कौन से हैं?",
        "answer": "Land disputes broadly fall into four categories:\n1. **Boundary & Encroachment Disputes**: Disputes over shifting field ridges (Mendh), illegal construction across borders, or overlapping cadastral coordinates.\n2. **Title & Ownership Disputes**: Competing claims over who is the true owner (e.g., fraudulent double-sale of same plot, disputed wills, forge sale deeds).\n3. **Co-Sharer & Family Partition Disputes**: Co-heirs refusing to divide ancestral land or disputes over road-facing front portions.\n4. **Landlord-Tenant / Possession Disputes**: Illegal squatters claiming adverse possession or tenants refusing to vacate.",
        "keywords": ["land disputes types", "bhu vivad", "jameen ka jhagda", "types of property dispute", "boundary conflict"],
        "state_notes": "Revenue disputes are decided by Revenue Courts (Tehsildar/SDM/Collector); Title disputes are decided by Civil Courts (Civil Judge/District Judge).",
        "related_questions": ["Where do I file a land dispute complaint?", "What to do if someone illegally occupies my land?", "How to check if land is under dispute?"]
    },
    {
        "id": "faq-disp-02",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "What should I do if someone illegally occupies or encroaches on my land?",
        "question_hi": "यदि कोई मेरी जमीन पर अवैध कब्जा कर ले तो तुरंत क्या कदम उठाने चाहिए?",
        "answer": "Follow these legal remedies immediately:\n1. **Police Complaint (Sec 447/427 IPC / BNS)**: Lodge an immediate FIR for criminal trespass and mischief at the local police station.\n2. **Section 145 CrPC Petition (SDM Court)**: If there is an imminent apprehension of breach of peace or violence, file a petition before the Sub-Divisional Magistrate (SDM). The SDM can attach the property and maintain status quo.\n3. **Section 24 Demarcation & Eviction**: For agricultural land, apply to the Tehsildar for demarcation. If encroachment is certified, the Tehsildar issues a 30-day eviction order with police assistance.\n4. **Civil Court Injunction Suit (Order 39 CPC)**: File a suit for Permanent Injunction and Possession under the Specific Relief Act 1963 before the Civil Judge.",
        "keywords": ["illegal occupation land", "kabza hataye", "encroachment complaint", "police complaint land trespass", "section 145 crpc"],
        "state_notes": "Special Anti-Land Mafia Task Forces operate in states like UP, Gujarat, and MP for registering complaints against habitual encroachers.",
        "related_questions": ["What is adverse possession?", "What is land demarcation?", "Where do I file a land dispute complaint?"]
    },
    {
        "id": "faq-disp-03",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "Where should I file a land dispute complaint (Revenue Court vs Civil Court)?",
        "question_hi": "जमीन विवाद की शिकायत कहां दर्ज करें — राजस्व न्यायालय या सिविल कोर्ट?",
        "answer": "The jurisdiction depends on the nature of the dispute:\n- **Revenue Courts (Tehsildar, SDM, Collector, Board of Revenue)**:\n  - For **boundary demarcation, shifting field ridges (Mendh), mutation (Dakhil-Kharij), correction of Khatauni/RoR errors, and division of agricultural holdings (Batwara)**.\n- **Civil Courts (Civil Judge, District Judge, High Court)**:\n  - For **declaration of title/ownership, cancellation of forged sale deeds, partition of non-agricultural properties, wills validity, and permanent injunctions against private individuals**.\n- Filing in the wrong forum results in dismissal for lack of jurisdiction.",
        "keywords": ["revenue court vs civil court", "where to file land dispute", "jurisdiction land dispute", "sdm vs civil judge", "tehsildar court power"],
        "state_notes": "Section 206 of UP Revenue Code bars Civil Courts from hearing matters exclusively assigned to Revenue Courts (like demarcation and mutation).",
        "related_questions": ["What is a land dispute?", "What is land demarcation?", "How to resolve boundary encroachment?"]
    },
    {
        "id": "faq-disp-04",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "What is a Stay Order (Temporary Injunction) on land and how do I get one?",
        "question_hi": "जमीन पर स्टे ऑर्डर (Stay Order / Injunction) कैसे लिया जाता है?",
        "answer": "A Stay Order (Temporary Injunction under Order 39 Rules 1 & 2 of CPC):\n- Prevents the opposing party from selling the land, creating third-party rights, constructing, or altering boundaries until the final lawsuit is decided.\n- **3 Essential Conditions to get a Stay**:\n  1. *Prima Facie Case*: You must show documents proving you have a strong genuine case.\n  2. *Balance of Convenience*: Tilts in your favor.\n  3. *Irreparable Injury*: You would suffer damage that money cannot compensate if the stay is denied.\n- File an application along with your main plaint supported by an urgent affidavit before the Civil Judge or Revenue Court.",
        "keywords": ["stay order land", "how to get stay order", "temporary injunction order 39", "jameen par stay", "stop sale stay order"],
        "state_notes": "Can also be obtained under Section 145 CrPC from Executive Magistrate / SDM in emergencies to prevent public clash.",
        "related_questions": ["How to check if land is under dispute?", "What should I do if someone illegally occupies my land?", "Where do I file a land dispute complaint?"]
    },
    {
        "id": "faq-disp-05",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "What is Lis Pendens (Section 52 of Transfer of Property Act)?",
        "question_hi": "लिस पेंडेंस (Lis Pendens / विचाराधीन वाद) का क्या नियम है?",
        "answer": "Under Section 52 of the Transfer of Property Act 1882:\n- During the pendency of any active lawsuit in court regarding title to immovable property, **neither party can transfer or sell the property** in a manner that affects the rights of the other party.\n- Any buyer who purchases land during a pending court lawsuit is bound by the court's ultimate decree, even if the buyer was unaware of the case.\n- Always check court portals (`ecourts.gov.in` and state revenue court systems) before buying to avoid purchasing a property locked under *lis pendens*.",
        "keywords": ["lis pendens", "section 52 transfer of property", "buying disputed property", "pending court case sale", "court case me jameen bechna"],
        "state_notes": "Some states (e.g. Maharashtra) require registration of notice of lis pendens at the Sub-Registrar office.",
        "related_questions": ["How to check if land is under dispute?", "What is a Stay Order?", "How to verify seller before buying?"]
    },
    {
        "id": "faq-disp-06",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "What to do if a fraudulent sale deed has been registered for my land?",
        "question_hi": "यदि किसी ने मेरी जमीन की फर्जी रजिस्ट्री करा ली है तो क्या करें?",
        "answer": "If someone fraudulently registers a forged deed for your property:\n1. **File Civil Suit for Cancellation**: File a suit for Cancellation of Void Deed and Declaration of Title before the Civil Judge under Section 31 of Specific Relief Act.\n2. **Criminal FIR (Section 420/467/468/471/120B IPC / BNS)**: Lodge an FIR against the imposter, buyer, and witnesses for fraud, forgery, and criminal conspiracy.\n3. **Stay / Injunction (Order 39 CPC)**: Immediately obtain an ex-parte stay order preventing further resale of the plot.\n4. **Intimate Sub-Registrar & Tehsildar**: Submit a formal caveat / objection with the SRO and Tehsildar with a copy of the FIR to block mutation.\n5. **Section 145 CrPC**: Apply to the SDM to maintain your physical possession.",
        "keywords": ["fraudulent sale deed", "farzi registry cancel", "fake registry complaint", "forged deed cancellation", "dhokhadhadi sale deed"],
        "state_notes": "In Tamil Nadu and Andhra Pradesh, Section 77A of Registration Act empowers District Registrars to cancel fraudulent registrations administratively.",
        "related_questions": ["What is a Stay Order?", "Where do I file a land dispute complaint?", "How to check if land is under dispute?"]
    },
    {
        "id": "faq-disp-07",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "What is Section 145 CrPC and how does it prevent land violence?",
        "question_hi": "धारा 145 सीआरपीसी (Section 145 CrPC) जमीन विवाद में कैसे काम करती है?",
        "answer": "Section 145 of the Code of Criminal Procedure (now Section 164 of BNSS 2023) is an emergency police/magisterial power to prevent bloodshed over land disputes:\n- When a dispute concerning land or boundaries is likely to cause a breach of peace or violent clash, the **Sub-Divisional Magistrate (SDM)** summons both parties.\n- The SDM does NOT decide legal title (which only civil courts do); the SDM investigates solely **who was in actual physical possession on the date of the police report**.\n- The SDM issues an order declaring that party entitled to possession until evicted by a competent civil court, and may attach the land under Section 146 CrPC in extreme cases.",
        "keywords": ["section 145 crpc", "sdm land possession dispute", "breach of peace land", "attachment of land section 146", "police report land clash"],
        "state_notes": "Widely utilized across rural India by District and Police Administration to defuse harvesting and demarcation clashes.",
        "related_questions": ["What should I do if someone illegally occupies my land?", "Where do I file a land dispute complaint?", "What is a Stay Order?"]
    },
    {
        "id": "faq-disp-08",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "What to do if an adjoining land owner blocks the path/road (Chak Road) to my agricultural field?",
        "question_hi": "यदि पड़ोसी खेत का रास्ता (चक रोड) रोक दे तो क्या कानूनी उपाय है?",
        "answer": "Blocking access to an agricultural plot is illegal under revenue and easement laws:\n1. **Check Revenue Map (Shajra)**: Check if the path is an official government Chak Road / Gata path.\n2. **Application under Section 25 (UP Revenue Code)**: Apply to the Tehsildar for restoration of customary village right of way or Chak Road. The Tehsildar can impose penalties and order removal of obstacles.\n3. **Section 133 CrPC (Public Nuisance)**: File a petition before the SDM for removal of unlawful obstruction on a public path.\n4. **Easement of Necessity**: Under Section 13 of the Indian Easements Act 1882, a landlocked parcel holder has an inherent legal right to access their plot.",
        "keywords": ["blocked farm road", "chak road kabza", "khet ka rasta band karna", "easement of necessity", "section 133 crpc road"],
        "state_notes": "Section 25 & 26 of UP Revenue Code 2006; Section 143 of Maharashtra Land Revenue Code (grant of way to landlocked cultivators).",
        "related_questions": ["What is Chakbandi?", "What is land demarcation?", "Where do I file a land dispute complaint?"]
    },
    {
        "id": "faq-disp-09",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "What is an Anti-Land Mafia Portal and how do I register a complaint?",
        "question_hi": "एंटी भू-माफिया पोर्टल (Anti-Land Mafia Portal) पर शिकायत कैसे दर्ज करें?",
        "answer": "Several states (such as Uttar Pradesh via the **Anti-Bhoo Mafia (IGRS) Portal**) have instituted special anti-land mafia task forces:\n- Dedicated to evicting organized criminals, encroachers, and land cartels illegally occupying private, Gram Sabha, or government lands.\n- **How to file**: Register a complaint on the state citizen grievance portal (e.g. `jansunwai.up.nic.in` under Anti-Bhoo Mafia category) with Khasra number, photos, and evidence.\n- A joint team of the Sub-Divisional Magistrate (SDM) and Circle Officer of Police (CO) investigates and registers FIRs under Gunda Act / Gangster Act if habitual mafia encroachment is found.",
        "keywords": ["anti bhoo mafia", "land mafia complaint", "jansunwai anti mafia", "land grabber complaint", "bhoo mafia portal"],
        "state_notes": "UP Anti-Bhoo Mafia Task Force operating since 2017; Gujarat Land Grabbing (Prohibition) Act 2020.",
        "related_questions": ["What should I do if someone illegally occupies my land?", "How to identify government land?", "Where do I file a land dispute complaint?"]
    },
    {
        "id": "faq-disp-10",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "Can a land dispute be resolved through Lok Adalat or Mediation?",
        "question_hi": "क्या जमीन विवाद लोक अदालत या मध्यस्थता (Mediation) से सुलझाया जा सकता है?",
        "answer": "Yes. Resolving through Lok Adalat or Court Mediation is often faster and cheaper than protracted court litigation:\n- **Lok Adalat (National / State)**: Partition disputes among family members, boundary demarcation compromises, and uncontested mutations can be settled mutually.\n- **Binding Decree**: An award passed by a Lok Adalat is deemed a decree of a Civil Court under the Legal Services Authorities Act 1987. **It is final and no appeal lies against it**.\n- **Full Refund of Court Fees**: If a pending court case is settled amicably in Lok Adalat, the entire court fee paid is refunded back to the parties.",
        "keywords": ["lok adalat land dispute", "mediation property dispute", "amicable settlement land", "samjhauta bhu vivad", "free court fee refund"],
        "state_notes": "Organized quarterly by National Legal Services Authority (NALSA) and State District Legal Services Authorities (DLSA).",
        "related_questions": ["What are common types of land disputes?", "Family partition of inherited land", "Where do I file a land dispute complaint?"]
    },
    {
        "id": "faq-disp-11",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "What is a Caveat and why should I file one in a land dispute?",
        "question_hi": "जमीन विवाद में कैविएट (Caveat / Section 148A CPC) क्या होती है?",
        "answer": "A Caveat is a formal legal notice filed under **Section 148A of the Civil Procedure Code** in a Civil or Revenue Court:\n- It directs the court: *'Do not pass any ex-parte stay order or interim decree against me without serving prior notice and hearing my defense.'*\n- **Validity**: A caveat remains valid for **90 days** from the date of filing.\n- If an opposing neighbor or hostile relative threatens to file a frivolous suit to obtain an ex-parte injunction behind your back, filing a caveat guarantees you will be notified.",
        "keywords": ["caveat petition", "section 148a cpc", "caveat land dispute", "prevent ex parte stay", "caveat kya hai"],
        "state_notes": "Can be filed in District Civil Courts, SDM Courts, and High Courts.",
        "related_questions": ["What is a Stay Order?", "Where do I file a land dispute complaint?", "How to check if land is under dispute?"]
    },
    {
        "id": "faq-disp-12",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "What happens if a co-owner constructs a building on joint undivided land without partition?",
        "question_hi": "यदि कोई सह-खातेदार बिना बंटवारे के संयुक्त जमीन पर मकान बना ले तो क्या करें?",
        "answer": "Under joint property law:\n1. Every co-owner has an undivided share across the whole parcel until a formal partition (Batwara) occurs.\n2. **No Co-owner Can Monopolize**: A single co-owner cannot unilaterally build on the best or front portion to the exclusion of other co-sharers.\n3. **Remedy**: Immediately file a suit for **Permanent Injunction (Order 39 CPC)** to halt construction, along with a **Suit for Division of Holding (Section 116 UP Revenue Code / Partition Suit)** to divide the plot by metes and bounds.",
        "keywords": ["construction on joint land", "co-owner illegal construction", "bina batware makan banana", "injunction against co-sharer"],
        "state_notes": "Settled under Section 116 of UP Revenue Code and Section 54 CPC.",
        "related_questions": ["What is joint ownership of land?", "Family partition of inherited land", "What is a Stay Order?"]
    },
    {
        "id": "faq-disp-13",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "What is an Injunction Suit under Specific Relief Act for property?",
        "question_hi": "जमीन के लिए निषेधाज्ञा (Injunction Suit) का मुकदमा क्या होता है?",
        "answer": "An Injunction Suit is filed under the Specific Relief Act 1963 before a Civil Judge to stop someone from interfering with your peaceful possession:\n- **Prohibitory Injunction**: Orders the defendant NOT to enter, trespass, build, or damage your land.\n- **Mandatory Injunction**: Compels the defendant to undo a wrongful act (e.g. demolish an encroaching wall built overnight).\n- Supported by revenue records (Khatauni), registered deed, and electricity/tax receipts showing actual possession.",
        "keywords": ["injunction suit", "specific relief act injunction", "nisheedhaghya mukadma", "civil suit possession", "restrain trespass"],
        "state_notes": "Governed by Sections 36-42 of Specific Relief Act 1963.",
        "related_questions": ["What is a Stay Order?", "Where do I file a land dispute complaint?", "What should I do if someone illegally occupies my land?"]
    },
    {
        "id": "faq-disp-14",
        "category": "Land Disputes",
        "category_id": "disputes",
        "question": "How do I check if my land is flagged as Disputed on this website?",
        "question_hi": "इस वेबसाइट पर मेरी जमीन विवादित (Disputed) है या नहीं कैसे जांचें?",
        "answer": "On this Intelligent Land Record Digitization system:\n1. Go to the **Citizen Portal** or **Overview** tab.\n2. Enter your Khasra Number (e.g. `102` or `105`) in the search bar.\n3. The system checks automated spatial geometry and ownership equity:\n   - **CLEAR Title**: Displayed in Green; 100% encumbrance-free.\n   - **WARNING Status**: Displayed in Amber; indicates share mismatch or low OCR confidence awaiting Patwari review.\n   - **DISPUTED Status**: Displayed in Red; indicates cadastral boundary overlap or duplicate conveyance.\n4. Click **Inspect in GIS** to view the exact overlapping red polygon on the satellite cadastral map.",
        "keywords": ["check dispute on website", "khasra status check", "disputed parcel search", "bhoomi dispute check", "red overlap polygon"],
        "state_notes": "Our system integrates live geodetic Shapely computational geometry and SHA-256 blockchain audit verification.",
        "related_questions": ["What is a Khasra number?", "How to resolve boundary encroachment?", "What are common types of land disputes?"]
    },

    # =========================================================================
    # CATEGORY 8: CORRECTION OF LAND RECORDS (12 FAQs)
    # =========================================================================
    {
        "id": "faq-cor-01",
        "category": "Correction of Land Records",
        "category_id": "correction",
        "question": "My name is misspelled in the Khatauni / land record. How do I correct it?",
        "question_hi": "खतौनी में नाम की स्पेलिंग गलत है, इसे कैसे ठीक कराएं?",
        "answer": "To correct a misspelled name in revenue records:\n1. **Section 38 Application (UP Revenue Code)**: File an application for correction of clerical / typographical error (दुरुस्ती / संशोधन) before the **Tehsildar / Sub-Divisional Officer (SDO)**.\n2. **Supporting Documents**: Submit registered Sale Deed, Aadhaar Card, PAN Card, Voter ID, and an affidavit affirming identity.\n3. **Patwari Report**: The SDO directs the Patwari to verify and report whether the applicant and the recorded person are the same individual.\n4. **Correction Order**: The SDO passes an order directing the registrar kanungo to correct the spelling in the live Khatauni.",
        "keywords": ["correct misspelled name", "wrong name in khatauni", "naam sudhar khatauni", "section 38 correction", "spelling mistake land record"],
        "state_notes": "Section 38 of UP Revenue Code 2006; Section 155 of Maharashtra Land Revenue Code; Section 13-B of Karnataka Land Revenue Act.",
        "related_questions": ["My father's name is wrong in land records. What should I do?", "How to correct wrong land area in revenue records?", "What documents are required for correction?"]
    },
    {
        "id": "faq-cor-02",
        "category": "Correction of Land Records",
        "category_id": "correction",
        "question": "My father's or husband's name is wrong in the land record. What should I do?",
        "question_hi": "खतौनी में पिता या पति का नाम गलत दर्ज है, क्या करें?",
        "answer": "If parentage or spouse name is incorrect:\n1. **File Correction Petition**: Apply under **Section 38** of the State Revenue Code before the Sub-Divisional Officer (SDO / Assistant Collector 1st Class).\n2. **Proof of Parentage**: Attach your School Leaving Certificate / 10th marksheet, Passport, Voter List extract, or Family Register (Parivar Register) showing correct parentage.\n3. **Registered Deed**: Present your registered purchase deed or ancestral succession document proving the original correct entry.\n4. **Order**: After verifying the Patwari report, the SDO orders the correction of parentage.",
        "keywords": ["father name wrong land record", "pita ka naam galat", "correction father name khatauni", "parentage correction revenue"],
        "state_notes": "Section 38 UP Revenue Code 2006; Rule 36 of UP Revenue Rules.",
        "related_questions": ["My name is misspelled in the Khatauni. How do I correct it?", "What documents are required for correction of land records?", "How to track correction requests?"]
    },
    {
        "id": "faq-cor-03",
        "category": "Correction of Land Records",
        "category_id": "correction",
        "question": "How to correct wrong land area (Rakba) in revenue records?",
        "question_hi": "खतौनी में रकबा (Area) गलत दर्ज हो गया है, इसे कैसे सुधरवाएं?",
        "answer": "If the area in the Khatauni is less or more than the registered title deed or consolidation map:\n1. **Inspect Consolidation Records**: Check the original C.H. Form 41/45 or Bandobast register to confirm whether the error occurred during computer digitization or consolidation.\n2. **File Area Correction Suit (Section 38(2))**: File a formal petition for Area Correction (रकबा दुरुस्ती) before the **Sub-Divisional Officer (SDO)**.\n3. **Joint Field Survey**: The SDO appoints the Revenue Inspector and Halka Patwari to physically measure all adjoining Khasra plots.\n4. **Hearing Adjoining Owners**: Adjoining landowners are summoned to ensure the area correction does not shrink their registered acreage.\n5. **Final Order**: The SDO orders the correction of the area in both the Khatauni and the GIS map.",
        "keywords": ["wrong land area", "rakba durusti", "area correction khatauni", "correct area in revenue record", "section 38 area correction"],
        "state_notes": "Section 38(2) of UP Revenue Code 2006; Section 106 of MLRC 1966.",
        "related_questions": ["What to do if on-ground area is smaller than Sale Deed?", "What is land demarcation?", "What is Map Correction (Naksha Durusti)?"]
    },
    {
        "id": "faq-cor-04",
        "category": "Correction of Land Records",
        "category_id": "correction",
        "question": "What is Map Correction (Naksha Durusti / Section 30)?",
        "question_hi": "नक्शा दुरुस्ती (Map Correction / Section 30) क्या होती है?",
        "answer": "Map Correction (Naksha Durusti) is the legal proceeding to correct mistakes in the village Cadastral Map (Shajra):\n- Often occurs when a plot's physical shape on the ground or area in the Khatauni does not match the printed map.\n- **Governing Law**: Section 30 of the UP Revenue Code 2006.\n- **Forum**: File petition before the **Collector / District Magistrate (DM)**.\n- **Process**: The Revenue Department re-measures the plot against base settlement points, draws an amended map (Tarmim), invites objections, and the Collector issues a decree modifying the official revenue map.",
        "keywords": ["map correction", "naksha durusti", "section 30 up revenue code", "shajra correction", "tarmim naksha"],
        "state_notes": "Section 30 of UP Revenue Code 2006; Section 106/107 of MLRC.",
        "related_questions": ["What is a Shajra?", "How to find plot boundaries?", "What to do when boundaries are incorrect?"]
    },
    {
        "id": "faq-cor-05",
        "category": "Correction of Land Records",
        "category_id": "correction",
        "question": "What documents are required for correcting land records?",
        "question_hi": "जमीन के रिकॉर्ड में सुधार कराने के लिए कौन से दस्तावेज चाहिए?",
        "answer": "To apply for record correction (दुरुस्ती):\n1. Application under Section 38 detailing the specific mistake and desired correction.\n2. Certified copy of the current erroneous Khatauni.\n3. Certified copy of the Registered Sale Deed / Partition Deed / Gift Deed proving the original true information.\n4. Certified copy of legacy consolidation records (C.H. Form 41, 45, or Bandobast Khatauni).\n5. Applicant's Government ID (Aadhaar, Voter ID, PAN).\n6. Affidavit on stamp paper affirming the facts.\n7. Court fee stamps as prescribed by state rules.",
        "keywords": ["documents for record correction", "khatauni sudhar documents", "durusti application kagajat"],
        "state_notes": "Can be submitted offline at Tehsil or online via state Revenue Court Management System portals.",
        "related_questions": ["My name is misspelled in the Khatauni. How do I correct it?", "My father's name is wrong in land records. What should I do?", "How to track correction requests?"]
    },
    {
        "id": "faq-cor-06",
        "category": "Correction of Land Records",
        "category_id": "correction",
        "question": "How do I correct a wrong Khasra or Survey number in a registered Sale Deed?",
        "question_hi": "रजिस्ट्री में खसरा नंबर गलत लिख गया हो तो उसे कैसे सुधारें?",
        "answer": "If a typographical error in the Khasra number occurred inside your registered Sale Deed:\n1. **Execute a Rectification Deed (Tatima Registry / Tattimnama)**: Both the buyer and the seller must visit the Sub-Registrar Office (SRO) and execute a registered Rectification Deed under Section 17 of the Registration Act.\n2. **State Specific Mistake**: The deed must explicitly state: *'In place of Khasra No. 101, it shall be read and understood as Khasra No. 102.'*\n3. **Stamp Duty**: Nominal stamp duty is payable if the area and consideration remain unchanged.\n4. **Submit for Mutation**: Submit the Rectification Deed to the Tehsildar to rectify the mutation entry.",
        "keywords": ["wrong khasra in sale deed", "rectification deed", "tatima registry", "tattimnama", "correct survey number deed"],
        "state_notes": "If the seller refuses to cooperate, the buyer must file a civil suit for rectification under Section 26 of Specific Relief Act 1963.",
        "related_questions": ["How property registration works?", "What are reasons for mutation rejection?", "How to correct wrong land area?"]
    },
    {
        "id": "faq-cor-07",
        "category": "Correction of Land Records",
        "category_id": "correction",
        "question": "How can I track the status of my record correction application?",
        "question_hi": "अभिलेख दुरुस्ती आवेदन की स्थिति (Status) कैसे ट्रैक करें?",
        "answer": "To track your correction petition:\n1. Visit your state's online Revenue Court Management System (e.g. UP Vaad `vaad.up.nic.in`, MP Saara RCMS, or Rajasthan Revenue Court).\n2. Search by **Case Number (वाद संख्या)** or **Section 38 Application Number**.\n3. The portal will show hearing dates, order sheets, whether the Patwari report has been received, and the final judgment order PDF.",
        "keywords": ["track correction request", "khatauni durusti status", "vaad portal case tracking", "revenue court status check"],
        "state_notes": "Available on UP Vaad portal, MP RCMS, and respective state revenue tracking platforms.",
        "related_questions": ["How to track mutation status?", "Where do I file a land dispute complaint?", "What documents are required for correction?"]
    },
    {
        "id": "faq-cor-08",
        "category": "Correction of Land Records",
        "category_id": "correction",
        "question": "What is Section 38 of the UP Revenue Code 2006?",
        "question_hi": "उत्तर प्रदेश राजस्व संहिता 2006 की धारा 38 क्या है?",
        "answer": "Section 38 of the UP Revenue Code 2006 empowers the revenue authorities to correct errors in the Record of Rights:\n- **Section 38(1)**: Clerical, arithmetical, or typographical errors in Khatauni are corrected by the Sub-Divisional Officer (SDO) or Tehsildar upon summary inquiry.\n- **Section 38(2)**: Material disputes regarding area (Rakba) or disputed title entries are adjudicated following formal notice to all affected parties.\n- Orders passed under Section 38 are appealable before the Divisional Commissioner within 30 days.",
        "keywords": ["section 38 up revenue code", "dhara 38 kya hai", "correction section 38", "clerical error correction up"],
        "state_notes": "Equivalent to Section 155 of Maharashtra Land Revenue Code 1966.",
        "related_questions": ["My name is misspelled in the Khatauni. How do I correct it?", "How to correct wrong land area in revenue records?", "What is Map Correction?"]
    },
    {
        "id": "faq-cor-09",
        "category": "Correction of Land Records",
        "category_id": "correction",
        "question": "Can land records be corrected if my name was omitted during computerization?",
        "question_hi": "क्या कम्प्यूटरीकरण के दौरान खतौनी से नाम छूट जाने पर नाम वापस दर्ज हो सकता है?",
        "answer": "Yes. During the digital scanning and computerization of legacy paper registers (Khatauni), typographical omissions occasionally occurred:\n1. Obtain a certified copy of the **pre-computerization hand-written Khatauni (Fasli register)** from the Tehsil Record Room showing your name was legitimately present.\n2. File an application before the SDO under Section 38 showing the pre-digital and post-digital comparison.\n3. The SDO verifies the manual archival register and orders restoration of your name into the live digital database.",
        "keywords": ["omitted name computerization", "computerized khatauni me naam gayab", "missing name digital land record", "data entry mistake khatauni"],
        "state_notes": "Commonly rectified under Special Camp drives organized by District Magistrates.",
        "related_questions": ["My name is misspelled in the Khatauni. How do I correct it?", "What is Section 38 of the UP Revenue Code?", "What is Record of Rights (RoR)?"]
    },
    {
        "id": "faq-cor-10",
        "category": "Correction of Land Records",
        "category_id": "correction",
        "question": "What is human-in-the-loop verification for OCR-digitized land records on this website?",
        "question_hi": "इस वेबसाइट पर कम कॉन्फिडेंस वाले रिकॉर्ड का सत्यापन कैसे होता है?",
        "answer": "On this system, when faded historical paper registers are ingested via Multilingual AI-OCR:\n- If ink fading or handwriting ambiguity yields field confidence < **85%**, the record is automatically routed to the **Review Queue**.\n- The Revenue Officer / Patwari inspects the side-by-side SVG digital facsimile of the original register, inputs certified correct values, and submits digital approval.\n- The verified values are permanently anchored into the SHA-256 blockchain audit ledger, raising confidence to 100%.",
        "keywords": ["human in the loop verification", "review queue patwari", "ocr confidence check", "faded ink verification", "blockchain record certification"],
        "state_notes": "Implemented directly in our system's 'Review Queue' tab for Patwaris.",
        "related_questions": ["How do I verify whether digital land record is genuine?", "How is land measured in India?", "What is a Khasra number?"]
    },
    {
        "id": "faq-cor-11",
        "category": "Correction of Land Records",
        "category_id": "correction",
        "question": "How to correct wrong caste or category (General/OBC/SC/ST) in land records?",
        "question_hi": "खतौनी में जाति या श्रेणी (Category) गलत दर्ज हो तो कैसे सुधरवाएं?",
        "answer": "If your social category or caste is misrecorded:\n1. Apply to the Tehsildar / SDO under Section 38.\n2. Submit your official **Government Caste Certificate (Jati Praman Patra)** issued by the competent district authority.\n3. Include an affidavit and legacy revenue records demonstrating ancestral family category.\n4. The SDO orders the correction in the revenue ledger to protect your statutory rights under land transfer laws.",
        "keywords": ["caste correction khatauni", "wrong category land record", "jati sudhar khatauni", "sc st category correction"],
        "state_notes": "Critical because SC/ST land enjoys statutory sale protection under state revenue codes.",
        "related_questions": ["Can land belonging to SC/ST be purchased?", "What documents are required for correction?", "My name is misspelled in the Khatauni. How do I correct it?"]
    },
    {
        "id": "faq-cor-12",
        "category": "Correction of Land Records",
        "category_id": "correction",
        "question": "How to remove an old cleared bank loan or mortgage from the Khatauni remarks column?",
        "question_hi": "बैंक लोन चुकने के बाद खतौनी से बंधक (Lien) कैसे हटवाएं?",
        "answer": "To remove (release) a cleared bank mortgage from revenue records:\n1. **Obtain No-Dues Certificate (NDC)**: Get a formal No-Dues Certificate and **Mortgage Release Letter** from the bank manager.\n2. **Bank Intimation to Tehsildar**: The bank issues a release intimation letter addressed to the Tehsildar / Sub-Registrar.\n3. **Application for Removal of Lien (बंधक मुक्ति)**: Submit the NDC and Release Letter to the Tehsildar office.\n4. **Amal-Daramad**: The Tehsildar orders the Patwari to delete the bank mortgage entry from Column 7/8 of the Khatauni, making the title unencumbered again.",
        "keywords": ["remove mortgage khatauni", "loan cleared remove lien", "bandhak mukti", "no dues certificate land", "delete bank loan entry"],
        "state_notes": "Integrated digitally in states like UP, MP, and Karnataka between banks and revenue portals.",
        "related_questions": ["How to check if land is mortgaged?", "What is an Encumbrance Certificate?", "What is Amal-Daramad?"]
    },

    # =========================================================================
    # CATEGORY 9: GOVERNMENT LAND AND RESTRICTIONS (12 FAQs)
    # =========================================================================
    {
        "id": "faq-gov-01",
        "category": "Government Land and Restrictions",
        "category_id": "govt_land",
        "question": "How can I identify whether a piece of land belongs to the Government or Gram Sabha?",
        "question_hi": "जमीन सरकारी या ग्राम सभा की है यह कैसे पहचानें?",
        "answer": "To identify government / public land:\n1. **Check Khata Category in Khatauni**:\n   - **Khata 1**: Private agricultural tenure holders (Bhumidhar).\n   - **Khata 5 & 6**: Government and Gram Sabha public utilities.\n2. **Key Keywords in Records**:\n   - **Nabin Parti** (Vacant barren land)\n   - **Banjar** (Uncultivated public land)\n   - **Gram Sabha / Gaon Sabha**\n   - **Khalihan** (Community threshing ground)\n   - **Charagah / Gochar** (Pasture land)\n   - **Pokhari / Talab** (Public pond/waterbody)\n   - **Kabristan / Shamshan** (Burial / Cremation grounds)\n   - **Chak Road / Rasta** (Public pathway)\n3. Any land listed under these categories is non-saleable public property.",
        "keywords": ["identify government land", "gram sabha land check", "sarkari jameen kaise pehchane", "banjar jameen", "charagah talab land"],
        "state_notes": "In UP, Section 77 of UP Revenue Code lists non-transferable public utility lands.",
        "related_questions": ["Can Gram Sabha or village common land be sold or purchased?", "What happens if someone encroaches on government land?", "What is agricultural vs residential land?"]
    },
    {
        "id": "faq-gov-02",
        "category": "Government Land and Restrictions",
        "category_id": "govt_land",
        "question": "Can Gram Sabha or village common land be legally sold, purchased, or regularized?",
        "question_hi": "क्या ग्राम सभा की जमीन खरीदी, बेची या नियमित कराई जा सकती है?",
        "answer": "No. Under the Supreme Court landmark ruling in *Jagpal Singh v. State of Punjab (2011)*:\n- Village common lands (Pond, Pasture, Grazing ground, Threshing floor, Cremation ground) are held by the Gram Sabha in trust for the entire village community.\n- **Cannot Be Sold**: Gram Sabha land cannot be transferred or sold to private individuals.\n- **No Adverse Possession or Regularization**: The Supreme Court ruled that illegal encroachment on village common lands CANNOT be regularized by state governments, even if the encroacher has built a house or paid fines.\n- Any private sale deed executed for Gram Sabha land is null, void, and a criminal offense.",
        "keywords": ["can gram sabha land be sold", "jagpal singh supreme court", "village common land sale", "regularize gram sabha encroachment"],
        "state_notes": "UP Revenue Code Section 77 explicitly prohibits allotment of ponds, pastures, and pathways.",
        "related_questions": ["How can I identify whether land belongs to Government?", "What happens if someone encroaches on government land?", "What is an Anti-Land Mafia Portal?"]
    },
    {
        "id": "faq-gov-03",
        "category": "Government Land and Restrictions",
        "category_id": "govt_land",
        "question": "What happens if someone encroaches on Government or Gram Sabha land (Section 67)?",
        "question_hi": "सरकारी या ग्राम सभा की जमीन पर कब्जा करने पर क्या कानूनी कार्रवाई होती है?",
        "answer": "Under Section 67 of the UP Revenue Code 2006 (and equivalent state eviction acts):\n1. **Notice in Form RC-20**: The Tehsildar / Assistant Collector issues a notice to the illegal encroacher.\n2. **Demolition & Eviction**: The administration orders physical demolition of unauthorized structures using bulldozers with police force.\n3. **Financial Damages**: Imposes heavy compensation/damages (Hajaana) equivalent to the market rate for the duration of illegal use.\n4. **Criminal Prosecution**: Habitual land encroachers are booked under the Public Property (Prevention of Damage) Act 1984.",
        "keywords": ["section 67 up revenue code", "eviction government land", "demolition gram sabha encroachment", "sarkari jameen se kabza hataye"],
        "state_notes": "Section 67 of UP Revenue Code 2006; Section 50 of MLRC 1966.",
        "related_questions": ["How can I identify whether land belongs to Government?", "Can Gram Sabha land be sold?", "What is an Anti-Land Mafia Portal?"]
    },
    {
        "id": "faq-gov-04",
        "category": "Government Land and Restrictions",
        "category_id": "govt_land",
        "question": "What is Section 80 / 143 (Agricultural to Non-Agricultural Conversion)?",
        "question_hi": "धारा 80 या 143 (जमीन का गैर-कृषि परिवर्तन) क्या है?",
        "answer": "Under Section 80 of the UP Revenue Code (formerly Section 143 of UPZA & LR Act):\n- Agricultural land cannot be used for residential, commercial, or industrial purposes without formal government declaration.\n- The landowner must apply to the Sub-Divisional Officer (SDO) for a declaration that the plot is used for non-agricultural purposes.\n- **Benefits of Section 80 Declaration**:\n  1. The land ceases to be governed by agricultural tenancy laws (no ceiling limits).\n  2. It can be partitioned, sold in small residential plots, or mortgaged for commercial loans.\n  3. You can obtain building map approval from town planning authorities.",
        "keywords": ["section 80 declaration", "section 143 conversion", "agricultural to non agricultural", "na conversion", "dhara 143 kya hai"],
        "state_notes": "Section 80 in UP; Section 44 of MLRC (NA order in Maharashtra); Section 95 of Karnataka Land Revenue Act.",
        "related_questions": ["What is agricultural land conversion?", "What are risks of unapproved colony plots?", "What documents are required to buy land?"]
    },
    {
        "id": "faq-gov-05",
        "category": "Government Land and Restrictions",
        "category_id": "govt_land",
        "question": "What is Forest Land (Section 4/20 Reserve Forest) and can it be bought?",
        "question_hi": "क्या वन भूमि (Forest Land) खरीदी जा सकती है?",
        "answer": "No. Forest land declared under Section 4 or Section 20 of the Indian Forest Act 1927 or Wildlife Protection Act 1972 cannot be private property:\n- Private sale deeds executed for reserve forest land are completely void.\n- Construction of resorts, houses, or farming on forest land is strictly prohibited under the Forest (Conservation) Act 1980.\n- Before buying land near hills, sanctuaries, or wooded zones, verify that the plot does not fall under the 'Orange Area' (disputed forest vs revenue classification).",
        "keywords": ["forest land sale", "section 4 forest act", "can forest land be bought", "van vibhag jameen", "wildlife sanctuary buffer zone"],
        "state_notes": "Protected under Forest (Conservation) Act 1980 and Supreme Court *Godavarman* guidelines.",
        "related_questions": ["How can I identify whether land belongs to Government?", "Can Gram Sabha land be sold?", "What are restricted and prohibited lands?"]
    },
    {
        "id": "faq-gov-06",
        "category": "Government Land and Restrictions",
        "category_id": "govt_land",
        "question": "What is Land Acquisition by the Government (LARR Act 2013) and how is compensation determined?",
        "question_hi": "सरकार जमीन का अधिग्रहण (Land Acquisition) कैसे करती है और मुआवजा कैसे तय होता है?",
        "answer": "Government acquires private land for public infrastructure (highways, railways, airports) under the **Right to Fair Compensation and Transparency in Land Acquisition, Rehabilitation and Resettlement Act (LARR Act 2013)**:\n- **Compensation Formula**:\n  - **Rural Areas**: Market Value (higher of circle rate or average sale price) × Multiplying Factor (1 to 2) + **100% Solatium** (mandatory bonus) = **Up to 4 times the market value**.\n  - **Urban Areas**: Market Value + 100% Solatium = **2 times the market value**.\n- Compensation is paid directly to bank accounts of landowners whose names are registered in the Khatauni.",
        "keywords": ["land acquisition act 2013", "larr act compensation", "sarkari adhigrahan muavza", "nhai land acquisition compensation", "4 times circle rate"],
        "state_notes": "National law applicable pan-India; direct purchase policies also operated by states for expressway projects.",
        "related_questions": ["How can I check who owns a piece of land?", "What happens if mutation is not done?", "What is Circle Rate?"]
    },
    {
        "id": "faq-gov-07",
        "category": "Government Land and Restrictions",
        "category_id": "govt_land",
        "question": "What is Prohibited Property (Section 22-A) and how do I avoid it?",
        "question_hi": "प्रतिबंधित संपत्ति (Section 22-A / Prohibited Properties) क्या है?",
        "answer": "Section 22-A of the Registration Act empowers state governments to notify a master **Prohibited Property List**:\n- Sub-Registrars are strictly forbidden from registering any deed involving these properties.\n- **Includes**: Waqf property, Bhoodan land, ceiling surplus land, government poramboke, temple/Devasthanam land, and assigned lands.\n- Portals (like Dharani in Telangana and Meeseva in AP) display a searchable Prohibited Property list. Always verify your survey number is not in this list before making a purchase.",
        "keywords": ["section 22 a registration act", "prohibited property list", "waqf land sale banned", "devasthanam land", "assigned land restriction"],
        "state_notes": "Section 22-A notified in AP, Telangana, Karnataka, and Tamil Nadu.",
        "related_questions": ["How can I identify whether land belongs to Government?", "Can Gram Sabha land be sold?", "How property registration works?"]
    },
    {
        "id": "faq-gov-08",
        "category": "Government Land and Restrictions",
        "category_id": "govt_land",
        "question": "What is Bhoodan Land and can it be sold?",
        "question_hi": "भूदान (Bhoodan) जमीन क्या होती है और क्या इसे बेचा जा सकता है?",
        "answer": "Bhoodan land refers to parcels donated by large landowners during Acharya Vinoba Bhave's Bhoodan Movement to be distributed to landless poor laborers (Asami/Pattadar):\n- The landless beneficiaries received **non-transferable usufructuary cultivation rights**.\n- **Bhoodan land CANNOT be sold, transferred, or mortgaged** to third parties.\n- Any sale deed executed for Bhoodan land is null and void, and the land automatically reverts to the Bhoodan Yagna Board or State Government.",
        "keywords": ["bhoodan land", "can bhoodan land be sold", "vinoba bhave bhoodan", "bhoodan yagna board", "landless grant sale prohibited"],
        "state_notes": "Governed by State Bhoodan Yagna Acts.",
        "related_questions": ["How can I identify whether land belongs to Government?", "Can Gram Sabha land be sold?", "What are restricted and prohibited lands?"]
    },
    {
        "id": "faq-gov-09",
        "category": "Government Land and Restrictions",
        "category_id": "govt_land",
        "question": "What is an Asami / Bhumidhar with Non-Transferable Rights?",
        "question_hi": "असंक्रमणीय भूमिधर (Bhumidhar with Non-Transferable Rights) क्या होता है?",
        "answer": "Under North Indian revenue codes, landowners are classified into categories:\n1. **Bhumidhar with Transferable Rights (संक्रमणीय भूमिधर)**: Holds permanent, inheritable, and fully transferable rights to sell or mortgage.\n2. **Bhumidhar with Non-Transferable Rights (असंक्रमणीय भूमिधर)**: Allotted land by the Gram Sabha for cultivation; can inherit but **CANNOT sell or transfer** to anyone.\n3. **Conversion to Transferable**: In UP, an Asami / non-transferable holder automatically becomes a transferable owner after **5 years** of peaceful cultivation under Section 76.",
        "keywords": ["asami", "bhumidhar with non transferable rights", "sankramaniya bhumidhar", "asankramaniya bhumidhar", "up revenue tenure types"],
        "state_notes": "Sections 74-77 of UP Revenue Code 2006.",
        "related_questions": ["How can I check who owns a piece of land?", "What is Khatauni?", "Can Gram Sabha land be sold?"]
    },
    {
        "id": "faq-gov-10",
        "category": "Government Land and Restrictions",
        "category_id": "govt_land",
        "question": "What is Lal Dora Land (लाल डोरा भूमि) in Delhi and Haryana?",
        "question_hi": "लाल डोरा (Lal Dora) जमीन क्या होती है?",
        "answer": "Lal Dora refers to the residential village abadi boundary drawn with red ink during British revenue surveys in 1908 in Delhi, Haryana, and Punjab:\n- **No Individual Cadastral Survey**: Historically, land inside the Lal Dora was exempt from building bye-laws and did not have individual Khasra survey numbers.\n- **SVAMITVA / Lal Dora Mukt Scheme**: Haryana and Delhi governments have undertaken drone surveys to grant formal digital ownership property cards to all Lal Dora residents.\n- While buying Lal Dora property, verify ownership through the SVAMITVA Property Card or Gram Panchayat register.",
        "keywords": ["lal dora land", "what is lal dora", "delhi lal dora", "haryana lal dora mukt", "lal dora property registry"],
        "state_notes": "Haryana became the first state to declare villages 'Lal Dora Free' under SVAMITVA Scheme.",
        "related_questions": ["What is the SVAMITVA Scheme?", "What is agricultural vs residential land?", "How property registration works?"]
    },
    {
        "id": "faq-gov-11",
        "category": "Government Land and Restrictions",
        "category_id": "govt_land",
        "question": "What are Wetland / Waterbody restrictions on land development?",
        "question_hi": "तालाब, पोखर या वेटलैंड जमीन पर निर्माण पर क्या प्रतिबंध हैं?",
        "answer": "Under Supreme Court rulings (*Hinch Lal Tiwari v. Kamala Devi*) and Wetlands (Conservation and Management) Rules:\n- Ponds (Pokhari), lakes (Talab), rivers, and designated wetlands cannot be filled, converted, or built upon even if private parties fraudulently procured a mutation entry.\n- Any construction on dried-up waterbodies is subject to immediate demolition by order of the High Court / NGT (National Green Tribunal).\n- Verify on the village Shajra map that your plot does not overlap with historical waterbody contours.",
        "keywords": ["wetland land restrictions", "talab pokhari construction ban", "hinch lal tiwari case", "ngt waterbody demolition", "pond land restriction"],
        "state_notes": "Enforced strictly by National Green Tribunal (NGT) and District Wetland Committees.",
        "related_questions": ["Can Gram Sabha land be sold?", "What is an Anti-Land Mafia Portal?", "How to identify government land?"]
    },
    {
        "id": "faq-gov-12",
        "category": "Government Land and Restrictions",
        "category_id": "govt_land",
        "question": "What is Coastal Regulation Zone (CRZ) restriction on coastal land?",
        "question_hi": "तटीय विनियमन क्षेत्र (CRZ) क्या है और क्या समुद्र किनारे जमीन पर निर्माण हो सकता है?",
        "answer": "Under the Coastal Regulation Zone (CRZ) Notification issued by Ministry of Environment, Forest and Climate Change (MoEFCC):\n- Land within 500 meters of the High Tide Line (HTL) along seas, bays, and estuaries is strictly regulated into CRZ-I (Ecologically sensitive), CRZ-II (Urban built-up), and CRZ-III (Rural coastal).\n- **No-Development Zone (NDZ)**: In CRZ-III rural coastal areas, no new construction is permitted within 200 meters of the High Tide Line.\n- Unapproved coastal villas or resorts face immediate demolition (such as the Maradu flats in Kerala).",
        "keywords": ["crz rules", "coastal regulation zone", "buying beach land", "no development zone 200m", "crz clearance"],
        "state_notes": "Enforced in Maharashtra, Goa, Kerala, Karnataka, Tamil Nadu, Andhra Pradesh, Odisha, and West Bengal.",
        "related_questions": ["Government land and restrictions", "What documents are required to buy land?", "Where to contact revenue department?"]
    },

    # =========================================================================
    # CATEGORY 10: DIGITAL LAND RECORDS AND ONLINE PORTALS (12 FAQs)
    # =========================================================================
    {
        "id": "faq-dig-01",
        "category": "Digital Land Records",
        "category_id": "digital_records",
        "question": "What are the major state land record portals across India?",
        "question_hi": "भारत के विभिन्न राज्यों के प्रमुख भूलेख पोर्टल कौन-कौन से हैं?",
        "answer": "Official state portals providing online land records:\n- **Uttar Pradesh**: UP Bhulekh (`upbhulekh.gov.in`)\n- **Maharashtra**: Mahabhulekh (`bhulekh.mahabhumi.gov.in`)\n- **Karnataka**: Bhoomi (`bhoomi.karnataka.gov.in`)\n- **Telangana**: Dharani (`dharani.telangana.gov.in`)\n- **Madhya Pradesh**: MP Bhulekh (`mpbhulekh.gov.in`)\n- **Bihar**: Bihar Bhumi (`biharbhumi.bihar.gov.in`)\n- **Rajasthan**: Apna Khata (`apnakhata.rajasthan.gov.in`)\n- **Punjab**: PLRS (`plrs.org.in` / `jamabandi.punjab.gov.in`)\n- **Haryana**: Jamabandi Haryana (`jamabandi.nic.in`)\n- **Gujarat**: AnyRoR (`anyror.gujarat.gov.in`)\n- **West Bengal**: Banglarbhumi (`banglarbhumi.gov.in`)\n- **Tamil Nadu**: AnyRoR / Patta Chitta (`eservices.tn.gov.in`)",
        "keywords": ["state land record portals", "bhulekh website list", "where to check land records online", "up bhulekh mahabhulekh bhoomi"],
        "state_notes": "All integrated under Central Government's Digital India Land Records Modernization Programme (DILRMP).",
        "related_questions": ["How to download land records online?", "How to verify digitally signed records?", "What is Record of Rights (RoR)?"]
    },
    {
        "id": "faq-dig-02",
        "category": "Digital Land Records",
        "category_id": "digital_records",
        "question": "How do I search for land records online using owner's name?",
        "question_hi": "मालिक के नाम से जमीन की खतौनी ऑनलाइन कैसे खोजें?",
        "answer": "To search land records by owner name:\n1. Open your state's Bhulekh portal (e.g. `upbhulekh.gov.in`).\n2. Select your **District, Tehsil, and Village**.\n3. Click on the tab **'Search by Name of Khatedar' (खातेदार के नाम द्वारा खोजें)**.\n4. Type the first few letters of the owner's name using the on-screen Hindi keyboard or standard phonetics.\n5. Select the matching name from the list and click 'View Extract' to view the complete Khatauni.",
        "keywords": ["search land record by name", "naam se khatauni khoje", "find plot by owner name", "online name search bhulekh"],
        "state_notes": "Available on UP Bhulekh, MP Bhulekh, Bihar Bhumi, and Haryana Jamabandi.",
        "related_questions": ["How can I check who owns a piece of land?", "What is a Khasra number?", "How to download land records online?"]
    },
    {
        "id": "faq-dig-03",
        "category": "Digital Land Records",
        "category_id": "digital_records",
        "question": "What is a Digitally Signed Land Record (Digital Signature Certificate / DSC)?",
        "question_hi": "डिजिटल हस्ताक्षरित खतौनी (Digitally Signed Khatauni) क्या होती है?",
        "answer": "A Digitally Signed Land Record is an electronic PDF document authenticated using a cryptographic Digital Signature Certificate (DSC) by the competent revenue authority (Tehsildar / Sub-Divisional Magistrate):\n- **Legal Validity**: Under Section 4 and 5 of the Information Technology Act 2000 and Section 65B of Indian Evidence Act, it has the **exact same legal standing as a physical stamped copy**.\n- No manual pen signature or rubber stamp from the Patwari is needed.\n- It contains a QR code that can be scanned by banks and courts to verify its tamper-proof authenticity.",
        "keywords": ["digitally signed khatauni", "dsc land record", "digital signature certificate", "legal validity digital ror", "it act 2000 land record"],
        "state_notes": "Available for nominal fee (₹15) on UP e-District, MP Bhulekh, Aaple Sarkar Maharashtra, and Bhoomi Karnataka.",
        "related_questions": ["How to verify digitally signed land records?", "What is QR code verification on land records?", "How to download land records online?"]
    },
    {
        "id": "faq-dig-04",
        "category": "Digital Land Records",
        "category_id": "digital_records",
        "question": "How does QR Code verification work on modern land records?",
        "question_hi": "खतौनी पर छपे क्यूआर कोड (QR Code) की जांच कैसे काम करती है?",
        "answer": "Every digitally certified revenue extract contains a secure QR code:\n1. Open any QR scanner or camera on your mobile phone.\n2. Scan the QR code printed on the top or bottom corner of the document.\n3. The scan immediately opens the official state government URL (`.gov.in` domain).\n4. The browser displays the exact live digital record stored in the government server.\n5. If the details on your paper match the webpage, the document is 100% genuine. If the link fails or displays different names, the paper document has been forged.",
        "keywords": ["qr code verification", "scan khatauni qr code", "check fake land document qr", "tamper proof qr code"],
        "state_notes": "Standardized across UP, Maharashtra, MP, Karnataka, and Telangana revenue extracts.",
        "related_questions": ["How to verify digitally signed land records?", "What is a Digitally Signed Land Record?", "How to check if land is under dispute?"]
    },
    {
        "id": "faq-dig-05",
        "category": "Digital Land Records",
        "category_id": "digital_records",
        "question": "What is BhuNaksha portal and how to download village cadastral map?",
        "question_hi": "भू-नक्शा (BhuNaksha) पोर्टल से खेत का नक्शा कैसे डाउनलोड करें?",
        "answer": "BhuNaksha (`bhunaksha.nic.in` or state specific subdomain) is a free national cadastral mapping software developed by NIC:\n1. Visit your state's BhuNaksha portal (e.g. `upbhunaksha.gov.in`, `mahabhunaksha.mahabhumi.gov.in`).\n2. Select your State, District, Tehsil, and Village.\n3. The interactive village map appears displaying all Khasra boundaries.\n4. Click on your specific Khasra / Survey number.\n5. Click on **'Plot Info / Map Report'** to download a certified printable PDF showing the exact boundary dimensions and neighbor Khasra numbers.",
        "keywords": ["bhunaksha portal", "download village map", "download khasra naksha", "khet ka naksha nikale", "cadastral map download"],
        "state_notes": "Operates seamlessly across 24+ states developed by National Informatics Centre (NIC).",
        "related_questions": ["What is a Shajra?", "What is land demarcation?", "What to do when boundaries are incorrect?"]
    },
    {
        "id": "faq-dig-06",
        "category": "Digital Land Records",
        "category_id": "digital_records",
        "question": "Can I access my land records on DigiLocker?",
        "question_hi": "क्या डिजिलॉकर (DigiLocker) पर जमीन के कागजात मिल सकते हैं?",
        "answer": "Yes. Under the Digital India initiative, state revenue departments are integrated with DigiLocker:\n1. Log into your **DigiLocker mobile app** or website using your Aadhaar.\n2. Search for your state Revenue Department (e.g., Department of Revenue - Uttar Pradesh, Maharashtra, or Karnataka).\n3. Select document type (e.g., 'Record of Rights' or 'Khatauni').\n4. Enter your District and Khata number.\n5. The digitally verified RoR is fetched directly from the state repository and stored in your Issued Documents folder, legally valid under Rule 9A of Information Technology Rules.",
        "keywords": ["digilocker land records", "khatauni on digilocker", "7 12 on digilocker", "digital land records app"],
        "state_notes": "Integrated across UP, Maharashtra, Karnataka, and Haryana.",
        "related_questions": ["What is a Digitally Signed Land Record?", "How to download land records online?", "What is QR code verification?"]
    },
    {
        "id": "faq-dig-07",
        "category": "Digital Land Records",
        "category_id": "digital_records",
        "question": "What is the ULPIN (Bhu-Aadhaar) 14-Digit Unique Land Parcel Identification Number?",
        "question_hi": "भू-आधार (ULPIN) का 14 अंकों का यूनिक नंबर क्या होता है?",
        "answer": "ULPIN (Unique Land Parcel Identification Number), also branded as **'Bhu-Aadhaar'**, is a central government initiative by the Department of Land Resources:\n- It assigns a unique **14-digit alphanumeric code** to every individual land parcel in India.\n- **How it is generated**: Based on the exact latitude-longitude geocoordinates of the parcel's corner vertices based on international WGS84 standards.\n- **Benefits**: Eliminates duplicate Khasra fraud, synchronizes registration with revenue records, prevents encroaching on public lands, and links seamlessly with bank mortgages.",
        "keywords": ["ulpin", "bhu aadhaar", "14 digit land id", "unique land parcel identification number", "bhu aadhaar card"],
        "state_notes": "Adopted in over 26 states including UP, Maharashtra, Bihar, and Andhra Pradesh.",
        "related_questions": ["What is a Khasra number?", "What is the SVAMITVA Scheme?", "What are government land records?"]
    },
    {
        "id": "faq-dig-08",
        "category": "Digital Land Records",
        "category_id": "digital_records",
        "question": "What to do if the online Bhulekh website shows an error or missing record?",
        "question_hi": "यदि ऑनलाइन भूलेख वेबसाइट पर रिकॉर्ड न दिखे या एरर आए तो क्या करें?",
        "answer": "If your record is missing on the Bhulekh portal:\n1. **Check Spelling & Khata Number**: Re-verify using the numerical Khata number rather than name spelling.\n2. **Ongoing Consolidation (Chakbandi)**: If Chakbandi is active in your village, online Khatauni viewing may be temporarily frozen until the new settlement is published.\n3. **Data Entry Error**: Apply to the Tehsildar / District Informatics Officer (DIO - NIC) with a physical copy of your previous Khatauni for missing data restoration.\n4. **Inspect Manual Register**: Visit the Tehsil Sub-Registrar / Record Room to check the physical paper Fasli register.",
        "keywords": ["bhulekh record missing", "khatauni nahi dikh rahi", "online land record error", "data not found bhulekh"],
        "state_notes": "NIC District Informatics Officer (DIO) handles technical database omissions.",
        "related_questions": ["Can land records be corrected if omitted during computerization?", "Where to contact revenue department?", "What is Chakbandi?"]
    },
    {
        "id": "faq-dig-09",
        "category": "Digital Land Records",
        "category_id": "digital_records",
        "question": "What is DILRMP (Digital India Land Records Modernization Programme)?",
        "question_hi": "डिजिटल इंडिया लैंड रिकॉर्ड्स मॉडर्नाइजेशन प्रोग्राम (DILRMP) क्या है?",
        "answer": "DILRMP is a flagship central sector programme by the Ministry of Rural Development, Government of India:\n- **Core Objectives**:\n  1. 100% computerization of land records (RoRs).\n  2. Digitization of cadastral maps (BhuNaksha) and spatial GIS integration.\n  3. Computerization of Sub-Registrar Offices (SROs) and automatic linking of registration with mutation.\n  4. Implementation of ULPIN (Bhu-Aadhaar).\n  5. Replacement of the current presumptive titling system with **conclusive land titling** with government-backed title guarantee.",
        "keywords": ["dilrmp", "digital india land records", "conclusive titling", "bhu aadhaar dilrmp", "land records modernization"],
        "state_notes": "Implemented across all 28 States and 8 Union Territories in India.",
        "related_questions": ["What is ULPIN (Bhu-Aadhaar)?", "What are major state land record portals?", "What are government land records?"]
    },
    {
        "id": "faq-dig-10",
        "category": "Digital Land Records",
        "category_id": "digital_records",
        "question": "How does blockchain technology prevent tampering of land records on this platform?",
        "question_hi": "इस प्लेटफॉर्म पर ब्लॉकचेन (Blockchain) तकनीक से जमीन के रिकॉर्ड में फर्जीवाड़ा कैसे रुकता है?",
        "answer": "On this Bhoomi system:\n1. **Cryptographic SHA-256 Chaining**: Every time a record is ingested, verified by an officer, or mutated, a cryptographic hash is generated linking it to the previous transaction.\n2. **Zero-Trust Immutability**: No individual, clerk, or hacker can silently alter a landowner's name, share percentage, or plot boundary in the database without immediately breaking the cryptographic chain.\n3. **Instant Tamper Detection**: The system continuously verifies hash integrity from Genesis to the latest block. Any unauthorized tampering triggers instant alerts.",
        "keywords": ["blockchain land records", "tamper proof land records", "sha-256 audit ledger", "prevent land fraud blockchain"],
        "state_notes": "State governments like Telangana, Maharashtra, and Karnataka are actively piloting blockchain for land registries.",
        "related_questions": ["How do I verify whether digital land record is genuine?", "What is ULPIN?", "What is a Digitally Signed Land Record?"]
    },
    {
        "id": "faq-dig-11",
        "category": "Digital Land Records",
        "category_id": "digital_records",
        "question": "What is the Dharani Portal in Telangana and why is it unique?",
        "question_hi": "तेलंगाना का धरणी (Dharani) पोर्टल क्या है और यह क्यों खास है?",
        "answer": "The **Dharani Portal** is Telangana's integrated land records management system:\n- **Single Window Integration**: Combines property registration and land mutation into a single simultaneous transaction. When you register a sale deed, the mutation occurs immediately in real time.\n- **Green Passbook**: Registered agricultural owners are issued a tamper-proof digital Pattadar Passbook.\n- **Prohibited Property Check**: Automated system blocks registration if the survey number falls under government, waqf, or court-disputed categories.",
        "keywords": ["dharani portal", "telangana dharani", "dharani slot booking", "pattadar passbook", "instant mutation dharani"],
        "state_notes": "Governed by Telangana Rights in Land and Pattadar Passbooks Act 2020.",
        "related_questions": ["What is Pahani / RTC?", "What is mutation?", "What is Prohibited Property?"]
    },
    {
        "id": "faq-dig-12",
        "category": "Digital Land Records",
        "category_id": "digital_records",
        "question": "What is AnyRoR in Gujarat?",
        "question_hi": "गुजरात का AnyRoR पोर्टल क्या है?",
        "answer": "AnyRoR (`anyror.gujarat.gov.in`) is the official portal of the Revenue Department of Gujarat:\n- Enables citizens to view and download:\n  - **VF7 (Village Form 7)**: Survey number and ownership details.\n  - **VF8A**: Khata holding summary.\n  - **VF6 (Mutation Register)**: History of all past property mutations.\n  - **Integrated Property Card**: For urban city survey properties.",
        "keywords": ["anyror gujarat", "anyror 7 12", "gujarat land records online", "vf7 vf8a anyror"],
        "state_notes": "Official portal of the Revenue Department of Gujarat.",
        "related_questions": ["What is a 7/12 Extract?", "What are major state land record portals?", "How to download land records online?"]
    },

    # =========================================================================
    # CATEGORY 11: PROPERTY REGISTRATION (14 FAQs)
    # =========================================================================
    {
        "id": "faq-reg-01",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "How does property registration work at the Sub-Registrar Office (SRO)?",
        "question_hi": "सब-रजिस्ट्रार कार्यालय (SRO) में जमीन की रजिस्ट्री कैसे होती है?",
        "answer": "The step-by-step registration procedure:\n1. **Drafting the Deed**: Draft the Sale Deed on legal paper with exact Khasra, area, boundaries, consideration amount, and buyer/seller terms.\n2. **Online Slot Booking & Stamp Duty**: Pay the calculated Stamp Duty and Registration charges online and book an SRO appointment.\n3. **Physical Appearance**: Buyer, Seller, and **Two Witnesses** must present themselves before the Sub-Registrar with original Aadhaar cards.\n4. **Biometric & Photo Capture**: Fingerprints and webcam photographs of all parties are recorded.\n5. **Registration & Endorsement**: The Sub-Registrar scrutinizes documents, asks verbal consent from the seller, registers the deed, and issues the official registered Sale Deed with unique document number.",
        "keywords": ["property registration process", "sro registry process", "jameen ki registry kaise hoti hai", "sub registrar office", "biometric registration"],
        "state_notes": "Governed by the Registration Act 1908 and Indian Stamp Act 1899.",
        "related_questions": ["What documents are required for property registration?", "What is Stamp Duty and Registration Fee?", "What is the difference between Agreement to Sell and Sale Deed?"]
    },
    {
        "id": "faq-reg-02",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "What documents are required for property registration at the SRO?",
        "question_hi": "रजिस्ट्री के समय कौन-कौन से दस्तावेज ले जाने अनिवार्य हैं?",
        "answer": "Mandatory documents for SRO registration:\n1. Original Drafted **Sale Deed / Conveyance Deed**.\n2. Proof of **Stamp Duty & Registration Fee payment** (e-Stamp certificate & challan).\n3. Original **Aadhaar Cards and PAN Cards** of Buyer, Seller, and 2 Witnesses.\n4. Latest certified **Record of Rights (Khatauni / 7-12 / Jamabandi copy)**.\n5. Form 60/61 (if buyer or seller does not hold a PAN card).\n6. Passport-sized photographs of all parties.\n7. Prior Title Deed chain copies.\n8. NOC / Permission letter (if property belongs to SC/ST or requires urban development clearance).",
        "keywords": ["documents required for registration", "registry documents checklist", "sro documents", "what to take for registry"],
        "state_notes": "Check state registration portal (e.g. IGRUP, IGR Maharashtra, Kaveri) for specific e-Challan requirements.",
        "related_questions": ["How property registration works?", "What is Stamp Duty and Registration Fee?", "Can land belonging to SC/ST be purchased?"]
    },
    {
        "id": "faq-reg-03",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "What is an e-Stamp Paper and how to verify its authenticity?",
        "question_hi": "ई-स्टाम्प पेपर (e-Stamp Paper) क्या है और इसकी जांच कैसे करें?",
        "answer": "An e-Stamp paper is an electronically generated stamp certificate issued by the Stock Holding Corporation of India Limited (SHCIL) or state treasury:\n- Replaces physical judicial stamp papers to prevent counterfeit stamp scams (like the Telgi stamp paper scam).\n- **Verification**: Go to the SHCIL e-Stamp verification portal (`shcilestamp.com`) or scan the certificate QR code.\n- Enter the Certificate Number, Stamp Duty Amount, and Date to ensure the certificate has not been used or cancelled.",
        "keywords": ["e-stamp paper", "shcil e-stamp", "verify e stamp certificate", "stamp paper verification", "electronic stamp paper"],
        "state_notes": "Used officially in Delhi, UP, Gujarat, Karnataka, Maharashtra, Rajasthan, and 20+ states.",
        "related_questions": ["What is Stamp Duty and Registration Fee?", "How property registration works?", "What is Circle Rate?"]
    },
    {
        "id": "faq-reg-04",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "What is a Gift Deed (Daan Patra) and can it be revoked?",
        "question_hi": "दान पत्र (Gift Deed) क्या होता है और क्या इसे रद्द किया जा सकता है?",
        "answer": "A Gift Deed is a registered instrument under Section 122 of the Transfer of Property Act transferring land voluntarily without any monetary consideration:\n- Must be accepted by the recipient (donee) during the lifetime of the donor.\n- **Revocation**: Once registered and accepted, **a Gift Deed CANNOT be revoked unilaterally** by the donor, unless the deed explicitly contained a specific conditional clause or fraud/undue influence is proven in Civil Court.\n- **Senior Citizens Act Exception**: Under the Maintenance and Welfare of Parents and Senior Citizens Act 2007, an elderly parent can petition the Maintenance Tribunal to cancel a gift deed if children fail to provide basic maintenance.",
        "keywords": ["gift deed", "daan patra", "can gift deed be cancelled", "senior citizen cancel gift deed", "revocation of gift deed"],
        "state_notes": "States like UP and Maharashtra offer heavily discounted stamp duty (e.g. ₹5,000 flat or 1%) for gift deeds executed between family members.",
        "related_questions": ["What is the difference between Agreement to Sell and Sale Deed?", "How property registration works?", "Who are legal heirs for land inheritance?"]
    },
    {
        "id": "faq-reg-05",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "What is a Lease Deed and when is registration mandatory?",
        "question_hi": "पट्टा विलेख (Lease Deed) क्या है और कब इसका पंजीकरण अनिवार्य है?",
        "answer": "Under Section 107 of the Transfer of Property Act and Section 17 of the Registration Act:\n- Any lease of immovable property from **year to year**, or for any term **exceeding one year**, or reserving a yearly rent, **must be made by a registered instrument**.\n- An unregistered lease deed for more than 11 months cannot be admitted as evidence in court to enforce terms.\n- This is why residential rent agreements are conventionally executed for **11 months** to avoid mandatory registration fees, although registering them offers stronger legal protection.",
        "keywords": ["lease deed", "11 month lease", "mandatory lease registration", "patta registration", "commercial lease registration"],
        "state_notes": "Governed by Registration Act 1908 and respective State Stamp Acts.",
        "related_questions": ["What is the difference between Freehold and Leasehold?", "How property registration works?", "What is Stamp Duty?"]
    },
    {
        "id": "faq-reg-06",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "What are the rules and role of Witnesses in property registration?",
        "question_hi": "रजिस्ट्री में गवाहों (Witnesses) की क्या भूमिका और नियम होते हैं?",
        "answer": "Under the Registration Act 1908:\n1. Exactly **two adult, competent witnesses** with valid photo ID (Aadhaar/Voter ID) must be physically present before the Sub-Registrar.\n2. **Role**: The witnesses do NOT guarantee title or verify boundaries; they testify that the seller and buyer signed the deed in their presence and identify the parties.\n3. **Liability**: If a seller impersonates someone else, witnesses who knowingly vouch for a fake seller face criminal prosecution for forgery and fraud under the Indian Penal Code.",
        "keywords": ["witness in registry", "gavah registry rules", "two witnesses registration", "witness liability forged deed"],
        "state_notes": "Biometrics of both witnesses are digitally recorded in modern digitized Sub-Registrar offices.",
        "related_questions": ["How property registration works?", "What documents are required for property registration?", "What to do if fraudulent sale deed registered?"]
    },
    {
        "id": "faq-reg-07",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "What is a Registered Will and is it mandatory to register a Will?",
        "question_hi": "रजिस्टर्ड वसीयत (Registered Will) क्या होती है और क्या वसीयत का रजिस्ट्रेशन अनिवार्य है?",
        "answer": "Under Section 18 of the Registration Act 1908:\n- **Registration of a Will is OPTIONAL**, not legally mandatory. An unregistered will written on plain paper attested by two witnesses is valid.\n- **Why Registration is Recommended**:\n  1. Proves the testator physically appeared before the Sub-Registrar with mental fitness.\n  2. Prevents allegations of forgery or manipulation by disgruntled family members after death.\n  3. A certified copy is preserved forever in the Sub-Registrar's secure vault, preventing destruction or loss.",
        "keywords": ["registered will", "is will registration mandatory", "vasiyat registration", "sub registrar will deposit"],
        "state_notes": "A will can be registered during the lifetime of the testator for a nominal fee at the SRO.",
        "related_questions": ["Can mutation be done based on an unregistered Will?", "Can an inherited ancestral property be given away by Will?", "Transfer of land after death of owner"]
    },
    {
        "id": "faq-reg-08",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "What is a Rectification Deed (Tattimnama) and when is it needed?",
        "question_hi": "संशोधन विलेख (Rectification Deed / ततीमा रजिस्ट्री) क्या होता है?",
        "answer": "A Rectification Deed (दुरुस्ती विलेख) is a registered deed executed to correct accidental clerical or typographical errors in a previously registered Sale Deed:\n- **Used for**: Correcting misspelled names, wrong plot numbers, wrong boundary descriptions, or typographical area errors.\n- **Prerequisites**: Both buyer and seller must agree mutually and appear at the Sub-Registrar Office to sign it.\n- **Limitation**: It cannot change the fundamental character of the transaction, change the buyer/seller, or increase the land area without paying additional stamp duty.",
        "keywords": ["rectification deed", "tattimnama", "durusti registry", "correct sale deed mistake", "amending registered deed"],
        "state_notes": "Section 17 of Registration Act 1908; Section 26 of Specific Relief Act 1963.",
        "related_questions": ["How to correct wrong survey or khasra number in Sale Deed?", "How property registration works?", "What documents are required for registration?"]
    },
    {
        "id": "faq-reg-09",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "Can property be registered online without visiting the Sub-Registrar Office?",
        "question_hi": "क्या बिना सब-रजिस्ट्रार कार्यालय जाए घर बैठे ऑनलाइन रजिस्ट्री हो सकती है?",
        "answer": "For absolute sale deeds, **physical presence remains mandatory** in most states:\n- Drafting, fee payment, stamp duty purchase, and slot booking are 100% online.\n- However, under Section 32A of the Registration Act, the physical presence of buyer, seller, and witnesses is legally required for biometric thumbprint authentication and live photo capture.\n- **Exceptions**: E-registration for leave & license (rental) agreements is fully paperless online in Maharashtra using Aadhaar e-Sign.",
        "keywords": ["online property registration", "ghar baithe registry", "e-registration sro", "can sale deed be registered online"],
        "state_notes": "Maharashtra offers complete remote e-Registration for 11-month rental agreements through IGR Maharashtra.",
        "related_questions": ["How property registration works?", "What documents are required for property registration?", "What is e-Stamp paper?"]
    },
    {
        "id": "faq-reg-10",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "What is Section 31 of Specific Relief Act regarding cancellation of registered deeds?",
        "question_hi": "रजिस्टर्ड बैनामा रद्द कराने की धारा 31 (Specific Relief Act) क्या है?",
        "answer": "Under Section 31 of the Specific Relief Act 1963:\n- A Sub-Registrar CANNOT cancel a registered sale deed once it has been executed.\n- Only a competent **Civil Court** has the power to adjudicate and cancel a registered deed on grounds of fraud, coercion, forgery, non-payment of consideration, or lack of title.\n- Once the Civil Judge passes a decree declaring the deed void, the court sends an official copy of the decree to the Sub-Registrar Office to make a formal cancellation entry in Book 1.",
        "keywords": ["section 31 specific relief act", "cancel registered sale deed", "bainama kharij suit", "civil court cancellation deed"],
        "state_notes": "Only Civil Courts have jurisdiction to cancel registered title deeds under law.",
        "related_questions": ["What to do if fraudulent sale deed registered?", "Where do I file a land dispute complaint?", "What is a Stay Order?"]
    },
    {
        "id": "faq-reg-11",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "What is an Index-II (इंडेक्स-2) in property registration?",
        "question_hi": "इंडेक्स-2 (Index-II) क्या होता है?",
        "answer": "Index-II is the official summary extract prepared and maintained by the Sub-Registrar Office for every registered property document:\n- It records: Names of buyer and seller, property description (survey number, boundaries, area), total consideration money paid, stamp duty paid, and registration date.\n- It serves as a public notice of the transaction.\n- In Maharashtra and Gujarat, downloading the Index-II from the IGR portal is standard practice to confirm that a deed was authentically archived.",
        "keywords": ["index ii", "what is index 2", "index 2 search online", "igr index 2 maharashtra", "registration summary extract"],
        "state_notes": "Maintained under Section 55 of the Registration Act 1908.",
        "related_questions": ["How property registration works?", "What is a 7/12 Extract?", "How to verify seller before buying?"]
    },
    {
        "id": "faq-reg-12",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "What is an NOC (No Objection Certificate) for land registration?",
        "question_hi": "जमीन रजिस्ट्री में NOC कब और क्यों लगती है?",
        "answer": "An NOC is a statutory clearance certificate from a government authority confirming no objection to the property transfer:\n- **Common Scenarios Requiring NOC**:\n  1. Transfer of tribal / SC land (Collector NOC).\n  2. Land situated near defense establishments, air force stations, or monuments (ASI NOC).\n  3. Industrial development authority plots (NOIDA / GIDC / KIADB NOC).\n  4. Forest boundary buffer zones.\n- Without a required NOC, the Sub-Registrar will refuse to register the deed.",
        "keywords": ["noc for land registration", "no objection certificate property", "when is noc needed registry", "collector noc land sale"],
        "state_notes": "Section 21 of Registration Act; State Town Planning and Ceiling guidelines.",
        "related_questions": ["Can land belonging to SC/ST be purchased?", "What documents are required for property registration?", "What is Prohibited Property?"]
    },
    {
        "id": "faq-reg-13",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "What happens if a property is undervalued during registration to save stamp duty?",
        "question_hi": "स्टाम्प ड्यूटी बचाने के लिए यदि रजिस्ट्री में कम मूल्य दिखाया जाए तो क्या होगा?",
        "answer": "Deliberate undervaluation to evade stamp duty is a serious legal offense:\n1. **Section 47-A Indian Stamp Act**: The Sub-Registrar can impound the deed and refer it to the Collector of Stamps for inquiry.\n2. **Heavy Penalty & Interest**: The Collector calculates the deficit stamp duty and levies penalties up to **4 to 10 times the deficit amount**, plus **1.5% monthly interest**.\n3. **Income Tax Notice (Section 56(2)(x) & 50C)**: The difference between circle rate and declared value is treated as taxable income in the hands of both buyer and seller.\n4. **Recovery Warrant**: Failure to pay results in revenue recovery warrants (Kurki) against the buyer's assets.",
        "keywords": ["property undervaluation", "section 47 a stamp act", "stamp duty evasion penalty", "section 50c income tax", "circle rate evasion"],
        "state_notes": "Enforced strictly under Section 47-A of the Indian Stamp Act 1899.",
        "related_questions": ["What is Circle Rate?", "What is Stamp Duty and Registration Fee?", "How property registration works?"]
    },
    {
        "id": "faq-reg-14",
        "category": "Property Registration",
        "category_id": "registration",
        "question": "What is an Exchange Deed (Badla-Patra) of land?",
        "question_hi": "जमीन की अदला-बदली (Exchange Deed / बदला-पत्र) क्या होती है?",
        "answer": "An Exchange Deed is a registered legal instrument under Section 118 of the Transfer of Property Act when two owners mutually agree to swap their plots:\n- Common between neighboring farmers to consolidate fragmented Chaks or access water channels.\n- **Stamp Duty**: Stamp duty is calculated only on the property of higher value (not both).\n- Both parties must complete mutual mutation (Dakhil-Kharij) to exchange their names in the respective Khataunis.",
        "keywords": ["exchange deed", "badla patra", "swap land plots", "section 118 transfer of property", "jameen ki adla badli"],
        "state_notes": "Governed by Section 118 of Transfer of Property Act 1882 and Section 79 of UP Revenue Code.",
        "related_questions": ["How property registration works?", "What is Chakbandi?", "What is mutation?"]
    },

    # =========================================================================
    # CATEGORY 12: LOANS AND MORTGAGES (11 FAQs)
    # =========================================================================
    {
        "id": "faq-loan-01",
        "category": "Loans and Mortgages",
        "category_id": "loans_mortgage",
        "question": "What land documents are required to take a bank agricultural or Kisan Credit Card (KCC) loan?",
        "question_hi": "किसान क्रेडिट कार्ड (KCC) या बैंक कृषि ऋण के लिए कौन-से कागजात चाहिए?",
        "answer": "To obtain an agricultural or KCC loan against land:\n1. **Latest Certified Khatauni / 7-12 / Jamabandi Copy**: Showing applicant's registered name with zero active disputes.\n2. **Land Possession Certificate (LPC)** or revenue inspector certificate confirming actual cultivation.\n3. **Nil-Encumbrance Certificate (EC - Form 16)**: Proving no prior mortgages exist.\n4. **No-Dues Certificate (NOC)** from nearby cooperative credit banks and commercial banks.\n5. **Aadhaar Card, PAN Card, and Land Revenue Tax Receipts**.\n6. **Soil / Crop Details**: Girdawari extract proving crop pattern for scale-of-finance calculation.",
        "keywords": ["documents for kcc loan", "bank agricultural loan land papers", "kisan credit card documents", "mortgage land for loan"],
        "state_notes": "Available under Reserve Bank of India (RBI) Priority Sector Lending and KCC guidelines.",
        "related_questions": ["What is an Encumbrance Certificate?", "How to check if land is mortgaged?", "What is a Land Possession Certificate (LPC)?"]
    },
    {
        "id": "faq-loan-02",
        "category": "Loans and Mortgages",
        "category_id": "loans_mortgage",
        "question": "How do I check whether a piece of land is already mortgaged to a bank?",
        "question_hi": "जमीन किसी बैंक में बंधक (Mortgage) है या नहीं यह कैसे पता करें?",
        "answer": "To check if land is currently mortgaged:\n1. **Check Column 7/8 (Remarks/Tippani) in Khatauni**: When a bank sanctions a loan, a formal charge / lien (Bandhak) is endorsed in the Khatauni remarks column (e.g. *'Mortgaged to SBI Sadar Branch for ₹5,00,000'*).\n2. **Apply for Encumbrance Certificate (EC)**: At the Sub-Registrar Office for the past 13 to 30 years.\n3. **Check CERSAI Registry (`cersai.org.in`)**: CERSAI (Central Electronic Registry of Securitisation Asset Reconstruction and Security Interest) maintains an online database of all bank mortgages across India.\n4. **Ask for Original Title Deeds**: Banks always retain the original registered title deed when granting a mortgage. If a seller shows only a photocopy, the original is likely pledged with a bank.",
        "keywords": ["check mortgaged land", "bandhak jameen check", "how to check bank loan on land", "cersai search", "mortgage verification"],
        "state_notes": "CERSAI search can be performed online by anyone on `cersai.org.in` for a nominal ₹10 fee.",
        "related_questions": ["What is an Encumbrance Certificate?", "How to verify seller before buying?", "How to remove cleared bank loan from Khatauni?"]
    },
    {
        "id": "faq-loan-03",
        "category": "Loans and Mortgages",
        "category_id": "loans_mortgage",
        "question": "What is an Equitable Mortgage vs Registered Mortgage on land?",
        "question_hi": "इक्विटेबल मॉर्गेज (Equitable) और रजिस्टर्ड मॉर्गेज (Registered Mortgage) में क्या अंतर है?",
        "answer": "- **Equitable Mortgage (Mortgage by Deposit of Title Deeds)**: Created by physically handing over the original registered title deeds to the bank lender with intent to create security. Does not necessarily require a full registered deed in some states, but is recorded in CERSAI.\n- **Registered Mortgage (Simple Mortgage)**: Formally drafted and registered at the Sub-Registrar Office (SRO) on non-judicial stamp paper. The mortgage charge is publicly indexed in SRO registers and updated in the government Khatauni.",
        "keywords": ["equitable mortgage vs registered mortgage", "deposit of title deeds", "simple mortgage", "mortgage types india"],
        "state_notes": "Section 58 of Transfer of Property Act 1882.",
        "related_questions": ["What is an Encumbrance Certificate?", "How to check if land is mortgaged?", "What land documents are required for a bank loan?"]
    },
    {
        "id": "faq-loan-04",
        "category": "Loans and Mortgages",
        "category_id": "loans_mortgage",
        "question": "What is CERSAI and how to do an online mortgage search?",
        "question_hi": "सरफेसी (CERSAI) पोर्टल क्या है और इसपर बंधक की जांच कैसे करें?",
        "answer": "CERSAI (`cersai.org.in`) is the central government online registry of security interests in property:\n- All banks, NBFCs, and financial institutions in India are legally mandated to register equitable and registered mortgages within 30 days of loan disbursement.\n- **Public Search**: Any citizen can conduct an 'Asset-Based Search' on the CERSAI portal by entering the plot number, survey number, and district to see which bank holds a financial charge against it.",
        "keywords": ["cersai search", "what is cersai", "check bank charge online", "cersai portal mortgage check"],
        "state_notes": "Established under Chapter IV of the SARFAESI Act 2002.",
        "related_questions": ["How to check if land is mortgaged?", "What is an Encumbrance Certificate?", "What is SARFAESI Act?"]
    },
    {
        "id": "faq-loan-05",
        "category": "Loans and Mortgages",
        "category_id": "loans_mortgage",
        "question": "Can a co-owner take a bank loan on their undivided share of joint land?",
        "question_hi": "क्या कोई सह-खातेदार संयुक्त जमीन में अपने हिस्से पर बैंक लोन ले सकता है?",
        "answer": "- **Agricultural KCC Loan**: Yes, a co-sharer can obtain a crop loan proportional to their documented share percentage.\n- **Mortgage / Term Loan**: Most commercial banks refuse to sanction mortgage loans on undivided joint shares without mutual consent or partition. Banks require all co-sharers to join as co-borrowers/guarantors, OR require a formal registered partition (Batwara) assigning an exclusive Khasra number.",
        "keywords": ["loan on joint land", "co-owner bank loan", "undivided share loan", "joint property mortgage"],
        "state_notes": "Subject to individual bank lending policies and Section 44 of Transfer of Property Act.",
        "related_questions": ["What is joint ownership of land?", "Family partition of inherited land", "What land documents are required for a bank loan?"]
    },
    {
        "id": "faq-loan-06",
        "category": "Loans and Mortgages",
        "category_id": "loans_mortgage",
        "question": "What is the SARFAESI Act and can a bank auction agricultural land?",
        "question_hi": "सरफेसी एक्ट (SARFAESI Act) क्या है और क्या बैंक कृषि भूमि की नीलामी कर सकता है?",
        "answer": "The SARFAESI Act 2002 empowers banks to auction mortgaged residential and commercial properties without going to court if the borrower defaults:\n- **Agricultural Land Exemption (Section 31(i))**: The SARFAESI Act **explicitly does NOT apply to agricultural land**.\n- A bank CANNOT enforce SARFAESI or seize farming land directly without filing a suit.\n- For agricultural loan recovery, banks must proceed through the State Agricultural Credit Operations Act, State Revenue Recovery Act (Tehsil recovery warrant / Kurki), or Debt Recovery Tribunal (DRT).",
        "keywords": ["sarfaesi act agricultural land", "can bank auction farm land", "section 31 i sarfaesi exemption", "bank loan default recovery"],
        "state_notes": "Supreme Court in *ITC Limited v. Blue Coast Hotels (2018)* confirmed agricultural land exemption under Section 31(i).",
        "related_questions": ["What is CERSAI?", "What is an Encumbrance Certificate?", "What land documents are required for a bank loan?"]
    },
    {
        "id": "faq-loan-07",
        "category": "Loans and Mortgages",
        "category_id": "loans_mortgage",
        "question": "What is an Attachment Order (Kurki / कुर्की) on land?",
        "question_hi": "जमीन की कुर्की (Attachment Order / Kurki) क्या होती है?",
        "answer": "Kurki (कुर्की / Property Attachment) is a court or revenue magistrate order attaching a debtor's land to recover unpaid debts or criminal penalties:\n- Once an attachment order is passed, it is noted in the Khatauni remarks column.\n- **Cannot Be Transferred**: Any sale, mortgage, or gift executed after an attachment order is void under Section 64 of CPC.\n- The District Collector can auction the land at public auction to recover government dues or bank arrears.",
        "keywords": ["kurki kya hai", "property attachment order", "section 64 cpc attachment", "revenue recovery kurki"],
        "state_notes": "Governed by Order 21 CPC and State Revenue Recovery Acts.",
        "related_questions": ["How to check if land is under dispute?", "What is an Encumbrance Certificate?", "How to remove cleared bank loan from Khatauni?"]
    },
    {
        "id": "faq-loan-08",
        "category": "Loans and Mortgages",
        "category_id": "loans_mortgage",
        "question": "How to obtain a formal No-Dues Certificate (NOC) from a bank?",
        "question_hi": "बैंक से नो-ड्यूज प्रमाणपत्र (No Dues Certificate) कैसे प्राप्त करें?",
        "answer": "Once you pay the final EMI or settlement amount of your land loan:\n1. Collect the official payment receipt showing zero outstanding balance.\n2. Submit a written letter requesting account closure, No Dues Certificate, and return of original title deeds.\n3. The bank issues a **No Objection Certificate / No Dues Certificate** on official letterhead within **30 days** (as mandated by recent RBI guidelines).\n4. If the bank delayed returning title deeds beyond 30 days, RBI mandates compensation of ₹5,000 per day of delay to the borrower.",
        "keywords": ["no dues certificate bank", "bank noc land", "mortgage release letter", "rbi compensation delayed title deeds"],
        "state_notes": "RBI circular on release of original property documents within 30 days enforced since Dec 2023.",
        "related_questions": ["How to remove cleared bank loan from Khatauni?", "What is an Encumbrance Certificate?", "What land documents are required for a bank loan?"]
    },
    {
        "id": "faq-loan-09",
        "category": "Loans and Mortgages",
        "category_id": "loans_mortgage",
        "question": "What is a 13-Point Title Clearance checklist used by Bank Panel Advocates?",
        "question_hi": "बैंक एडवोकेट द्वारा टाइटल क्लीयरेंस के 13 मुख्य बिंदु कौन से होते हैं?",
        "answer": "Bank legal panels assess these 13 points before issuing a Title Clearance Certificate (TCC):\n1. 30-year unbroken chain of title deeds.\n2. Current unencumbered Khatauni / 7-12 in borrower's name.\n3. Nil-Encumbrance Certificate (Form 16) for 13–30 years.\n4. No active court stay or *lis pendens*.\n5. Zero co-sharer equity mismatch (100% share verified).\n6. No SC/ST transfer restriction breach.\n7. Approved layout sanction / Section 80/143 conversion (for residential plots).\n8. Certified BhuNaksha map showing physical access road.\n9. Up-to-date land tax receipts.\n10. CERSAI search report clear.\n11. Physical site inspection confirmation (no squatter).\n12. All borrower and guarantor identity KYC verified.\n13. Valuation report by approved chartered valuer.",
        "keywords": ["13 point title checklist", "bank title clearance report", "tcc report bank loan", "advocate title search bank"],
        "state_notes": "Standardized Indian Banks' Association (IBA) due diligence framework.",
        "related_questions": ["What is an Encumbrance Certificate?", "How to verify seller before buying?", "What is a 30-Year Search Report?"]
    },
    {
        "id": "faq-loan-10",
        "category": "Loans and Mortgages",
        "category_id": "loans_mortgage",
        "question": "What happens if a bank loses my original land title deeds?",
        "question_hi": "यदि बैंक मेरे जमीन के मूल कागजात (Original Title Deeds) खो दे तो क्या करें?",
        "answer": "Under RBI Master Directive on Release of Movable/Immovable Property Documents:\n1. **Bank Must Bear All Costs**: The bank must lodge a police complaint (FIR), publish public loss notices in newspapers, and pay all expenses to obtain certified copies from the SRO.\n2. **Bank Issues Certificate of Loss**: The bank must issue an official certificate confirming that the original deed was lost while in its custody.\n3. **Monetary Penalty on Bank**: If the bank fails to return or replace the documents within 30 days of full loan repayment, it must pay the borrower **₹5,000 per day** of delay.",
        "keywords": ["bank lost original deeds", "rbi rule lost title deeds", "penalty on bank lost papers", "fir lost land registry"],
        "state_notes": "Governed by RBI Notification RBI/2023-24/60 applicable to all commercial and cooperative banks.",
        "related_questions": ["How to obtain No-Dues Certificate?", "What is an Equitable Mortgage?", "How property registration works?"]
    },
    {
        "id": "faq-loan-11",
        "category": "Loans and Mortgages",
        "category_id": "loans_mortgage",
        "question": "Can I take a loan on ancestral agricultural land without dividing it?",
        "question_hi": "क्या बिना बंटवारे के पैतृक कृषि भूमि पर लोन मिल सकता है?",
        "answer": "- **KCC Crop Loan**: Yes, co-sharers can take crop loans on their respective share fraction if all co-owners sign NOCs or become co-borrowers.\n- **Commercial / Housing Loan**: No. For construction or mortgage loans, banks strictly require individual demarcated plots with exclusive boundary boundaries. Partition (Batwara) under Section 116 is essential before applying.",
        "keywords": ["loan on undivided ancestral land", "kcc on ancestral land", "paitrik jameen par loan"],
        "state_notes": "Cooperative banks grant individual KCC limits based on undivided Khata holding.",
        "related_questions": ["What is joint ownership of land?", "Family partition of inherited land", "What land documents are required for a bank loan?"]
    },

    # =========================================================================
    # CATEGORY 13: AGRICULTURAL LAND (11 FAQs)
    # =========================================================================
    {
        "id": "faq-agr-01",
        "category": "Agricultural Land",
        "category_id": "agricultural",
        "question": "What is Agricultural to Non-Agricultural (NA) land conversion?",
        "question_hi": "कृषि भूमि को गैर-कृषि (NA / Section 143/80) में कैसे बदलें?",
        "answer": "Agricultural to Non-Agricultural conversion is the formal government procedure to change land use classification from farming to residential, commercial, or industrial:\n- **Governing Law**: Section 80 of UP Revenue Code 2006; Section 44 of MLRC 1966; Section 95 of Karnataka Land Revenue Act.\n- **Process**:\n  1. Apply online via state revenue portal (e.g. e-District UP, Mahabhumi NA portal).\n  2. Submit Khatauni, BhuNaksha map, proposed building layout plan, and identity proof.\n  3. Revenue Inspector inspects the field to verify that the land is not Gram Sabha, pond, or road reserve.\n  4. Pay the statutory conversion fee (calculated as a percentage of circle rate).\n  5. Sub-Divisional Officer (SDO / Collector) passes the formal Conversion Order.",
        "keywords": ["agricultural to residential conversion", "na order", "land use conversion", "section 80 conversion", "kheti ki jameen par makan"],
        "state_notes": "Called 'Section 80' in UP (formerly 143), 'NA Order' in Maharashtra/Gujarat, 'CLU' (Change of Land Use) in Haryana/Punjab.",
        "related_questions": ["What is Section 80/143 declaration?", "What are risks of unapproved colony plots?", "Can agricultural land be used for commercial business?"]
    },
    {
        "id": "faq-agr-02",
        "category": "Agricultural Land",
        "category_id": "agricultural",
        "question": "Can I build a house on agricultural land without converting it (Section 143/80)?",
        "question_hi": "क्या बिना 143 कराए खेत में मकान बनाया जा सकता है?",
        "answer": "- **Small Farmhouse / Residence for Cultivator**: Most state revenue codes permit a farmer to build a small farmhouse or dwelling strictly for agricultural management on a small portion of their own field without conversion.\n- **Commercial / Plotted Residential Colony**: Strictly ILLEGAL without an official Section 80 / NA conversion order. Authorities can demolish the structure, seal the premises, and cancel registration under urban planning laws.",
        "keywords": ["build house on farm land without conversion", "khet me makan banana", "farmhouse permission", "bina 143 makan banana"],
        "state_notes": "Section 80(2) of UP Revenue Code exempts small residential units below specified limits for personal agricultural use.",
        "related_questions": ["What is Agricultural to Non-Agricultural land conversion?", "What are risks of unapproved colony plots?", "What is Section 80 declaration?"]
    },
    {
        "id": "faq-agr-03",
        "category": "Agricultural Land",
        "category_id": "agricultural",
        "question": "What is Change of Land Use (CLU) in Haryana and Punjab?",
        "question_hi": "हरियाणा और पंजाब में सीएलयू (CLU / Change of Land Use) क्या होता है?",
        "answer": "CLU (Change of Land Use) is the formal permission granted by the Town and Country Planning Department in Haryana and Punjab:\n- Mandatory before setting up any residential colony, commercial warehouse, factory, school, or petrol pump on agricultural land.\n- Requires payment of internal development charges (IDC) and external development charges (EDC).\n- Operating a commercial business without CLU attracts heavy fines and disconnection of electricity.",
        "keywords": ["clu haryana", "change of land use punjab", "what is clu", "clu permission process"],
        "state_notes": "Regulated by Haryana Town and Country Planning Department and Punjab PUDA.",
        "related_questions": ["What is Agricultural to Non-Agricultural land conversion?", "What are risks of unapproved colony plots?", "What is Circle Rate?"]
    },
    {
        "id": "faq-agr-04",
        "category": "Agricultural Land",
        "category_id": "agricultural",
        "question": "What are the restrictions on selling fragmented pieces of agricultural land?",
        "question_hi": "खेत का छोटा टुकड़ा (Fragmented Land) बेचने पर क्या रोक है?",
        "answer": "Under state **Prevention of Fragmentation Acts**:\n- Governments prohibit sub-dividing agricultural land below a minimum viable size (Standard Acre / Fragment):\n  - In Uttar Pradesh, an agricultural parcel cannot normally be fragmented below **3.125 Acres (5 Bighas)** unless the adjacent neighbor purchases it or it is converted under Section 80.\n  - In Maharashtra, selling fragments below the statutory 'Tukdebandi' limit is prohibited under the Bombay Prevention of Fragmentation Act 1947.\n- Unlawful fragmented sale deeds cannot be mutated in revenue records.",
        "keywords": ["fragmentation of land", "tukdebandi act", "minimum agricultural plot size", "chhota tukda bechna manahi"],
        "state_notes": "UP Revenue Code Section 89; Bombay Prevention of Fragmentation and Consolidation of Holdings Act 1947.",
        "related_questions": ["What is Chakbandi?", "What is Agricultural to Non-Agricultural land conversion?", "Reasons for mutation rejection"]
    },
    {
        "id": "faq-agr-05",
        "category": "Agricultural Land",
        "category_id": "agricultural",
        "question": "Can a tenant or sharecropper (Bataidar / Sikmi) claim ownership of agricultural land?",
        "question_hi": "क्या बटाईदार (Bataidar) या काश्तकार जमीन पर मालिकाना हक का दावा कर सकता है?",
        "answer": "Under modern land reforms laws:\n- Landowners commonly give agricultural fields to sharecroppers (Bataidar / Adhiya) for seasonal cultivation.\n- A tenant **CANNOT claim ownership** if the lease is temporary or informal.\n- However, to prevent tenant disputes:\n  1. Landowners should ensure their own name is entered in the seasonal **Girdawari / Pik-Pahani** crop survey.\n  2. Avoid executing long-term undocumented leases exceeding statutory tenancy thresholds.\n  3. Use Model Agricultural Land Leasing Act contracts which legally protect the landowner's absolute title while ensuring tenant crop loans.",
        "keywords": ["bataidar ownership claim", "sharecropper rights", "tenant claiming land", "khet batayi par dena", "model land leasing act"],
        "state_notes": "NITI Aayog Model Agricultural Land Leasing Act adopted by MP and UP protects landowners against tenancy claims.",
        "related_questions": ["What is adverse possession?", "What is Girdawari?", "What to do if someone illegally occupies my land?"]
    },
    {
        "id": "faq-agr-06",
        "category": "Agricultural Land",
        "category_id": "agricultural",
        "question": "What is the Model Agricultural Land Leasing Act?",
        "question_hi": "मॉडल एग्रीकल्चरल लैंड लीजिंग एक्ट क्या है?",
        "answer": "Formulated by NITI Aayog to modernize agricultural tenancy:\n1. Allows land owners to legally lease agricultural land to tenant farmers through written mutual agreements.\n2. **Absolute Protection for Landowner**: Guarantees that the tenant can NEVER claim adverse possession or tenancy ownership rights, regardless of lease duration.\n3. **Benefit for Tenant**: Enables the tenant cultivator to access institutional crop loans (KCC), crop insurance, and disaster relief without needing the landowner's title deed.",
        "keywords": ["model land leasing act", "niti aayog land lease", "kheti lease agreement", "legal farmland leasing"],
        "state_notes": "Enacted in MP (Bhoomi Swami evam Batai-dar Adhiniyam 2016) and UP Revenue Code amendments.",
        "related_questions": ["Can a tenant claim ownership?", "What are land documents required for a bank loan?", "What is Girdawari?"]
    },
    {
        "id": "faq-agr-07",
        "category": "Agricultural Land",
        "category_id": "agricultural",
        "question": "Can I set up a solar power plant on agricultural land?",
        "question_hi": "क्या कृषि भूमि पर सोलर प्लांट लगाया जा सकता है?",
        "answer": "Yes, setting up a solar power plant is widely encouraged under government green energy policies (like PM KUSUM):\n- In many states, solar energy generation is granted deemed non-agricultural status or expedited Section 80 / NA permission.\n- Farmers can lease their dry/unirrigated agricultural land to solar developers for 25-year lease periods with long-term rental income.\n- Check with your state renewable energy development agency (e.g. UPNEDA, MEDA, KREDL).",
        "keywords": ["solar plant on agricultural land", "pm kusum scheme", "solar lease farmland", "solar land conversion"],
        "state_notes": "Exempted from stringent conversion fees in Rajasthan, Gujarat, UP, and Karnataka.",
        "related_questions": ["What is Agricultural to Non-Agricultural land conversion?", "What is the difference between Freehold and Leasehold?", "How property registration works?"]
    },
    {
        "id": "faq-agr-08",
        "category": "Agricultural Land",
        "category_id": "agricultural",
        "question": "What is PM-Kisan Samman Nidhi and how is it linked to land records?",
        "question_hi": "पीएम किसान सम्मान निधि (PM-Kisan) के लिए जमीन के रिकॉर्ड का सत्यापन कैसे होता है?",
        "answer": "Under the PM-Kisan scheme, eligible landholding farmer families receive ₹6,000 per year in three installments:\n- **Mandatory Land Seeding**: The farmer's name must be officially registered in the state Khatauni / RoR database.\n- **e-KYC & Land Verification**: The portal cross-verifies the farmer's Aadhaar with the digital land record database (Bhu-Aadhaar).\n- If your PM-Kisan installment is stopped due to 'Land Seeding: No', submit your verified Khatauni to your local Agriculture Officer or Lekhpal to update the portal.",
        "keywords": ["pm kisan land seeding", "pm kisan samman nidhi", "pm kisan ekyc land record", "khatuni seeding pm kisan"],
        "state_notes": "Managed online via `pmkisan.gov.in`.",
        "related_questions": ["What is Khatauni?", "How to download land records online?", "Where to contact the Patwari?"]
    },
    {
        "id": "faq-agr-09",
        "category": "Agricultural Land",
        "category_id": "agricultural",
        "question": "What is organic / contract farming agreement registration?",
        "question_hi": "अनुबंध खेती (Contract Farming) क्या होती है?",
        "answer": "Contract farming is an agreement between an agricultural producer (farmer) and a buyer (food processor or corporate) specifying terms for the production and supply of agricultural products:\n- **Ownership Protected**: The agreement is purely for purchase of produce; the buyer cannot mortgage or claim title to the farmer's land.\n- Must be registered with the local APMC / District Agriculture Office.",
        "keywords": ["contract farming", "anubandh kheti", "corporate contract farming rules", "farmer title protection contract farming"],
        "state_notes": "Governed by State APMC Acts and Contract Farming Rules.",
        "related_questions": ["Can a tenant claim ownership?", "What is agricultural land ceiling limit?", "What is Girdawari?"]
    },
    {
        "id": "faq-agr-10",
        "category": "Agricultural Land",
        "category_id": "agricultural",
        "question": "What is Gaon Sabha pasture land (Charagah / Gauchar) and can it be cultivated?",
        "question_hi": "गौचर या चारागाह की जमीन पर क्या खेती की जा सकती है?",
        "answer": "No. Gauchar (Charagah / Pasture land) is strictly reserved for cattle grazing under the ownership of the Gram Sabha:\n- Any person cultivating or fencing Gauchar land is an illegal trespasser liable for eviction under Section 67.\n- The Supreme Court has repeatedly held that pasture land cannot be reclassified or regularized for farming.",
        "keywords": ["charagah land", "gauchar jameen", "pasture land farming illegal", "gram sabha charagah"],
        "state_notes": "Supreme Court *Jagpal Singh (2011)* judgment strictly protects pasture land.",
        "related_questions": ["How can I identify whether land belongs to Government?", "Can Gram Sabha land be sold?", "What happens if someone encroaches on government land?"]
    },
    {
        "id": "faq-agr-11",
        "category": "Agricultural Land",
        "category_id": "agricultural",
        "question": "What is the difference between Irrigated (Sinchit) and Unirrigated (Asinchit) land in revenue records?",
        "question_hi": "सिंचित (Sinchit) और असिंचित (Asinchit) जमीन में क्या अंतर है?",
        "answer": "- **Sinchit (Irrigated Land)**: Land served by assured perennial water sources (tube-well, canal, river). It yields higher productivity, commands higher circle rates, and has a lower land ceiling limit (e.g. 12.5 acres in UP).\n- **Asinchit (Unirrigated / Barren Land)**: Dependent purely on rainfall (dry land). It has lower circle rates, lower land revenue tax, and a higher permissible ceiling limit (up to 18 to 54 acres depending on state).",
        "keywords": ["sinchit vs asinchit", "irrigated vs unirrigated land", "ceiling limit irrigated land", "malguzari tax difference"],
        "state_notes": "Indicated in Village Form Part A of Khatauni and Girdawari registers.",
        "related_questions": ["What is agricultural land ceiling limit?", "What is Khatauni?", "What is Girdawari?"]
    },

    # =========================================================================
    # CATEGORY 14: CITIZEN HELP AND REVENUE ADMINISTRATION (14 FAQs)
    # =========================================================================
    {
        "id": "faq-hlp-01",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "What are the roles of Patwari (Lekhpal / Talathi) in land administration?",
        "question_hi": "पटवारी / लेखपाल / तलाठी के मुख्य कार्य क्या होते हैं?",
        "answer": "The Patwari (called **Lekhpal** in UP, **Talathi** in Maharashtra, **Karnam/VAO** in Tamil Nadu, **Village Revenue Officer (VRO)** in Andhra/Telangana) is the primary grassroots village revenue official:\n- **Key Responsibilities**:\n  1. Maintains and updates the village Record of Rights (Khatauni / Jamabandi / 7-12).\n  2. Conducts seasonal crop surveys (Girdawari / Pik-Pahani).\n  3. Conducts field inquiries for mutation (Dakhil-Kharij) and succession (Virasat).\n  4. Measures plot boundaries during demarcation alongside the Revenue Inspector.\n  5. Reports encroachments on Gram Sabha and government lands.\n  6. Assesses crop damage during floods, droughts, or hailstorms for disaster relief.",
        "keywords": ["patwari duties", "lekhpal ke kaam", "talathi role", "who is patwari", "village revenue officer"],
        "state_notes": "Every village is grouped under a revenue circle called 'Patwari Halka'.",
        "related_questions": ["Where can I meet the Patwari?", "What is the role of a Tehsildar?", "How to file a complaint against a Patwari?"]
    },
    {
        "id": "faq-hlp-02",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "What is the role and jurisdiction of a Tehsildar and Naib Tehsildar?",
        "question_hi": "तहसीलदार और नायब तहसीलदार के अधिकार और कार्य क्या हैं?",
        "answer": "- **Tehsildar / Naib Tehsildar**:\n  - Head of the Tehsil (Taluka) revenue administration and acts as an Assistant Collector / Revenue Court Magistrate.\n  - **Judicial Powers**:\n    1. Adjudicates and passes legally binding orders in **Mutation (Dakhil-Kharij)** cases.\n    2. Decides boundary disputes and Section 24 demarcation petitions.\n    3. Issues orders for removal of encroachments on public land (Section 67).\n    4. Issues Domicile, Caste, and Income Certificates.\n    5. Supervises land revenue collection and recovery warrants.",
        "keywords": ["tehsildar powers", "naib tehsildar role", "tehsildar court", "what does tehsildar do", "revenue magistrate"],
        "state_notes": "Appeals against Tehsildar orders lie before the Sub-Divisional Officer (SDO / SDM).",
        "related_questions": ["What is the role of a Patwari?", "Where do I file a land dispute complaint?", "What is the role of an SDM?"]
    },
    {
        "id": "faq-hlp-03",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "What is the role of the Sub-Divisional Magistrate (SDM / SDO)?",
        "question_hi": "उप-जिलाधिकारी (SDM / SDO) के भूमि से जुड़े अधिकार क्या हैं?",
        "answer": "The Sub-Divisional Officer (SDO) / Sub-Divisional Magistrate (SDM) heads the administrative sub-division (comprising several tehsils):\n- **Key Powers in Land Matters**:\n  1. Hears **Appeals** against orders passed by Tehsildars in mutation cases.\n  2. Trials suits for **Partition of agricultural land (Section 116 Batwara)**.\n  3. Adjudicates **Area Correction (Rakba Durusti - Section 38(2))**.\n  4. Decides applications for **Agricultural to Non-Agricultural Conversion (Section 80/143)**.\n  5. Exercises preventive criminal jurisdiction under **Section 145 CrPC** to maintain possession and stop violent clashes.",
        "keywords": ["sdm powers land", "sdo revenue court", "sub divisional magistrate role", "sdm appeal mutation", "prant officer"],
        "state_notes": "Known as Sub-Divisional Officer (SDO) or Sub-Divisional Magistrate (SDM) in North India, Prant Officer in Maharashtra.",
        "related_questions": ["What is the role of a Tehsildar?", "Where do I file a land dispute complaint?", "Family partition of inherited land"]
    },
    {
        "id": "faq-hlp-04",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "Where can I meet the Patwari / Lekhpal and what are his working hours?",
        "question_hi": "पटवारी / लेखपाल से कहां और कब मिल सकते हैं?",
        "answer": "- **Tehsil / Halka Office**: Lekhpals and Patwaris are scheduled to be present at their assigned Tehsil Halka Office on designated days (commonly **Tuesdays and Fridays**, or during **Tehsil Diwas / Sampoorna Samadhan Diwas**).\n- **Panchayat Bhawan**: Present during Gram Sabha meetings and village revenue camps.\n- **Contact Information**: You can find your assigned Lekhpal's official mobile number on your district's official website (`district.nic.in`) or via state portals like UP Bhulekh 'Know Your Lekhpal' (अपने लेखपाल को जानें).",
        "keywords": ["how to find patwari", "where to meet lekhpal", "lekhpal contact number", "apne lekhpal ko jane", "tehsil diwas"],
        "state_notes": "In UP, search Lekhpal contact directly on `upbhulekh.gov.in`.",
        "related_questions": ["What are the roles of Patwari?", "How to file a complaint against a Patwari?", "What is Tehsil Diwas?"]
    },
    {
        "id": "faq-hlp-05",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "How can I file an online grievance or complaint regarding land issues?",
        "question_hi": "जमीन संबंधित मामलों की ऑनलाइन शिकायत (Grievance) कैसे दर्ज करें?",
        "answer": "You can file official grievances through state Citizen Grievance Redressal Portals:\n1. **State Portals**: Log into portals like **Jansunwai IGRS (UP)** (`jansunwai.up.nic.in`), **CM Helpline (MP 181)**, **Aaple Sarkar (Maharashtra)**, or **Prajavani (Telangana)**.\n2. **Central Portal**: For central government or inter-state matters, lodge a complaint on **CPGRAMS** (`pgportal.gov.in`).\n3. **Tracking**: You receive an SMS tracking number. The concerned SDM/Tehsildar must submit a time-bound action-taken report within **15 to 30 days**.",
        "keywords": ["file land complaint online", "jansunwai up", "cm helpline complaint land", "cpgrams land grievance", "bhu vivad shikayat"],
        "state_notes": "Jansunwai in UP; CM Helpline 181 in MP; Aaple Sarkar in Maharashtra; Spandana in AP.",
        "related_questions": ["What is Tehsil Diwas?", "How to file a complaint against a Patwari?", "Where to contact revenue department?"]
    },
    {
        "id": "faq-hlp-06",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "What is Tehsil Diwas (Sampoorna Samadhan Diwas)?",
        "question_hi": "तहसील दिवस (सम्पूर्ण समाधान दिवस) क्या होता है?",
        "answer": "Tehsil Diwas (Sampoorna Samadhan Diwas) is a bi-monthly direct public grievance hearing organized at the Tehsil headquarters:\n- **Schedule**: Held on the **1st and 3rd Tuesdays** of every month (or 1st and 3rd Saturdays in some states).\n- **High-Level Attendance**: Attended in person by the **District Magistrate (DM), Senior Superintendent of Police (SSP), Sub-Divisional Magistrate (SDM), Tehsildar, and Block Development Officer (BDO)**.\n- **Direct Action**: Citizens can personally submit written petitions regarding illegal encroachment, delayed mutation, broken boundary stones, or corrupt officials. Many spot inquiries and immediate resolutions are ordered on the same day.",
        "keywords": ["tehsil diwas", "sampoorna samadhan diwas", "dm hearing tehsil", "direct public grievance land"],
        "state_notes": "Held across all 75 districts of Uttar Pradesh and similar patterns in MP, Bihar, and Rajasthan.",
        "related_questions": ["How can I file an online grievance?", "Where to contact revenue department?", "What should I do if someone illegally occupies my land?"]
    },
    {
        "id": "faq-hlp-07",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "How to file a complaint if a Patwari / Lekhpal demands a bribe or delays work?",
        "question_hi": "यदि लेखपाल / पटवारी काम में देरी करे या रिश्वत मांगे तो क्या करें?",
        "answer": "If a revenue official demands an illegal bribe or intentionally delays statutory work:\n1. **Complaint to Higher Revenue Officers**: Submit a written complaint to the **Sub-Divisional Magistrate (SDM) or District Magistrate (DM)**.\n2. **Public Grievance Portal**: File an urgent complaint on the CM Helpline / Jansunwai portal naming the official and your pending application number.\n3. **Anti-Corruption Bureau (ACB / Vigilance)**: Contact your State Anti-Corruption Bureau (ACB / Vigilance Directorate Helpline). ACB conducts official trap operations to catch corrupt officials red-handed.\n4. **Right to Public Services Act**: File a penalty appeal under your state's Guarantee of Services Act for everyday delay beyond statutory limits.",
        "keywords": ["complaint against patwari", "lekhpal rishwat shikayat", "anti corruption helpline land", "patwari delay complaint"],
        "state_notes": "Vigilance toll-free numbers: UP (1064 / 9454401866), Maharashtra ACB (1064), MP Lokayukta.",
        "related_questions": ["What is Tehsil Diwas?", "What is the statutory time limit for mutation?", "How can I file an online grievance?"]
    },
    {
        "id": "faq-hlp-08",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "How can I file an RTI (Right to Information) application for land records?",
        "question_hi": "जमीन के पुराने रिकॉर्ड या नक्शे के लिए आरटीआई (RTI) कैसे लगाएं?",
        "answer": "Under the Right to Information (RTI) Act 2005:\n1. **Identify Public Authority**: The Public Information Officer (PIO) is typically the **Tehsildar / Sub-Divisional Officer (SDO)** of the respective Tehsil.\n2. **Draft Application**: Specify the exact information sought (e.g., *'Certified copy of Mutation Order dated 12/04/1998 for Khasra 105 in Village Rampur'*).\n3. **Application Fee**: Pay the nominal ₹10 fee via Postal Order, Treasury Challan, or online via State RTI portal (`rtionline.gov.in`).\n4. **30-Day Mandatory Deadline**: The PIO must provide the requested information within **30 days**. If denied, file a First Appeal before the First Appellate Authority (SDM/ADM).",
        "keywords": ["rti for land records", "right to information land", "jameen par rti kaise lagaye", "tehsildar rti application"],
        "state_notes": "Governed by Central RTI Act 2005; applicable pan-India.",
        "related_questions": ["Where can I get certified copies of old revenue records?", "How to verify digitally signed records?", "What are government land records?"]
    },
    {
        "id": "faq-hlp-09",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "Where can I get certified copies of 50 or 100-year-old historical revenue records (Bandobast)?",
        "question_hi": "50 या 100 साल पुराने ऐतिहासिक राजस्व अभिलेख (बंदोबस्त / मिसल हकियत) कहां मिलते हैं?",
        "answer": "For pre-independence or historical records:\n1. **District Collectorate Record Room (Muhafizkhana / अभिलेखागार)**: Maintains colonial settlement records, original Bandobast Missal Hakiyat, and historical Shajra maps.\n2. **Tehsil Record Room**: Holds Fasli Khatauni registers from the past 12 to 30 years.\n3. **Apply for Certified Copy (Nakal)**: Fill out a Copying Application (नकल दरख्वास्त) at the Collectorate Copying Section specifying Village name, Pargana, and approximate settlement year.\n4. **State Archives**: For records older than 1857, visit your State Central Archives (e.g. UP State Archives Lucknow, Maharashtra State Archives Mumbai).",
        "keywords": ["old land records", "muhafizkhana", "missal hakiyat", "bandobast record copy", "100 year old land records"],
        "state_notes": "Maintained in Collectorate Record Rooms in every District Headquarters.",
        "related_questions": ["What is a 30-Year Search Report?", "What is Fasli Year?", "What is Chakbandi?"]
    },
    {
        "id": "faq-hlp-10",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "What is the role of District Magistrate (DM / Collector) in land administration?",
        "question_hi": "भूमि प्रशासन में जिलाधिकारी (DM / Collector) की क्या भूमिका होती है?",
        "answer": "The District Magistrate (DM / Collector / Deputy Commissioner) is the **highest revenue authority in the district**:\n- **Chief Revenue Officer**: Custodian of all government and public lands in the district.\n- **Court of the Collector**: Hears appeals in land revenue cases, approves non-transferable SC/ST land transfers, and adjudicates Section 30 Map Correction disputes.\n- **Collector of Stamps**: Decides cases of stamp duty undervaluation under Section 47-A.\n- **Land Acquisition Authority**: Heads government land acquisition proceedings under the LARR Act 2013.",
        "keywords": ["district magistrate role land", "collector powers land", "dm court land appeal", "chief revenue officer"],
        "state_notes": "Appeals against Collector's orders lie before the Divisional Commissioner and Board of Revenue.",
        "related_questions": ["What is the role of an SDM?", "What is Map Correction?", "What is Section 47-A Stamp Duty?"]
    },
    {
        "id": "faq-hlp-11",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "What is the Board of Revenue (राजस्व परिषद)?",
        "question_hi": "राजस्व परिषद (Board of Revenue) क्या है?",
        "answer": "The Board of Revenue is the **highest appellate authority and apex court in a state for land revenue disputes**:\n- Functions as the supreme court of revenue administration, just below the High Court.\n- Hears second appeals, revision petitions, and supervisory review against orders passed by Divisional Commissioners and Collectors.\n- Formulates rules, revenue codes, and oversees land record digitization across the entire state.",
        "keywords": ["board of revenue", "rajaswa parishad", "apex revenue court", "revenue appeal board"],
        "state_notes": "Board of Revenue UP (Lucknow/Prayagraj); Maharashtra Revenue Tribunal (MRT Mumbai); Board of Revenue Rajasthan (Ajmer).",
        "related_questions": ["Where do I file a land dispute complaint?", "What is the role of District Magistrate?", "What is a Tehsildar?"]
    },
    {
        "id": "faq-hlp-12",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "What are Common Service Centers (CSC / Jan Seva Kendra) and how do they help in land services?",
        "question_hi": "जन सेवा केंद्र (CSC / Jan Seva Kendra) से जमीन की कौन-सी सेवाएं मिलती हैं?",
        "answer": "Common Service Centers (CSC / VLEs / Jan Seva Kendra) are authorized government digital kiosks in rural and urban areas:\n- **Services Offered**:\n  1. Print certified copies of Khatauni / 7-12 / Jamabandi.\n  2. Apply online for mutation (Dakhil-Kharij) and Varisatan succession.\n  3. Download BhuNaksha village cadastral maps.\n  4. Apply for Income, Caste, and Domicile certificates.\n  5. Complete PM-Kisan e-KYC and land seeding.\n- CSCs charge fixed, government-regulated service charges (usually ₹15 to ₹30 per application).",
        "keywords": ["csc center land services", "jan seva kendra khatauni", "csc bhu abhilekh", "village kiosk land records"],
        "state_notes": "Operating across all Gram Panchayats in India under Digital India.",
        "related_questions": ["How to download land records online?", "How do I apply for mutation?", "What are major state land record portals?"]
    },
    {
        "id": "faq-hlp-13",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "What is the Legal Services Authority (DLSA) and how to get free legal aid for land disputes?",
        "question_hi": "भूमि विवाद में मुफ्त कानूनी सहायता (Free Legal Aid / DLSA) कैसे प्राप्त करें?",
        "answer": "Under the Legal Services Authorities Act 1987:\n- The **District Legal Services Authority (DLSA)**, located at every District Court, provides **free advocates and waives court fees** for eligible citizens:\n  - Women and children\n  - Members of Scheduled Castes (SC) and Scheduled Tribes (ST)\n  - Agricultural laborers and low-income individuals (annual income below ₹3 Lakhs in most states)\n- Visit the DLSA office at your District Court or apply online via `nalsa.gov.in` to get a government-funded advocate to represent you in land disputes.",
        "keywords": ["free legal aid land dispute", "dlsa free lawyer", "nalsa free legal help", "muft vakil zameen vivad"],
        "state_notes": "Offices located at all District and Taluka Court complexes pan-India.",
        "related_questions": ["Can a land dispute be resolved through Lok Adalat?", "Where do I file a land dispute complaint?", "What are common types of land disputes?"]
    },
    {
        "id": "faq-hlp-14",
        "category": "Citizen Help",
        "category_id": "citizen_help",
        "question": "What are the standard government fees for common land record services?",
        "question_hi": "विभिन्न भू-अभिलेख सेवाओं के लिए सरकारी फीस कितनी होती है?",
        "answer": "Typical government fees under state Citizen Charters:\n- **Viewing Online Records**: 100% Free on all state Bhulekh portals.\n- **Certified Digitally Signed Khatauni / 7-12**: ₹10 to ₹20 per extract.\n- **Certified Village Cadastral Map (BhuNaksha)**: ₹10 to ₹25.\n- **Demarcation (Section 24 Seemankan)**: ₹1,000 per boundary pillar.\n- **Mutation Application (Undisputed)**: ₹30 to ₹100 nominal court fee.\n- **Encumbrance Certificate (EC)**: ₹100 to ₹300 depending on number of search years.\n- Never pay unauthorized bribes; always demand an official computerized treasury receipt.",
        "keywords": ["land records government fees", "khatauni nikalne ki sarkari fees", "mutation fee", "demarcation fee", "bhu naksha charge"],
        "state_notes": "Statutory fees fixed under State Financial Handbooks and Revenue Codes.",
        "related_questions": ["What is the statutory time limit for mutation?", "How to download land records online?", "How do I apply for Section 24 demarcation?"]
    }
]

# Quick lookup indexes
FAQS_BY_ID = {faq["id"]: faq for faq in LAND_FAQ_DATABASE}
FAQS_BY_CATEGORY = {}
for faq in LAND_FAQ_DATABASE:
    cat = faq["category_id"]
    if cat not in FAQS_BY_CATEGORY:
        FAQS_BY_CATEGORY[cat] = []
    FAQS_BY_CATEGORY[cat].append(faq)

FAQ_CATEGORIES = [
    {"id": "ownership", "name": "Land Ownership & Verification", "name_hi": "भूमि स्वामित्व एवं सत्यापन", "icon": "fa-shield-alt"},
    {"id": "records", "name": "Land Records & Terminology", "name_hi": "भू-अभिलेख एवं शब्दावली", "icon": "fa-file-invoice"},
    {"id": "mutation", "name": "Mutation (Dakhil-Kharij)", "name_hi": "दाखिल-खारिज / नामांतरण", "icon": "fa-exchange-alt"},
    {"id": "buying_selling", "name": "Buying Land & Due Diligence", "name_hi": "जमीन खरीद एवं धोखाधड़ी से बचाव", "icon": "fa-shopping-cart"},
    {"id": "inheritance", "name": "Inheritance & Partition", "name_hi": "विरासत, उत्तराधिकार एवं बंटवारा", "icon": "fa-users"},
    {"id": "measurement", "name": "Demarcation & Measurement", "name_hi": "सीमांकन, पैमाइश एवं नक्शा", "icon": "fa-ruler-combined"},
    {"id": "disputes", "name": "Disputes & Revenue Courts", "name_hi": "भूमि विवाद एवं राजस्व न्यायालय", "icon": "fa-gavel"},
    {"id": "correction", "name": "Record Correction (Durusti)", "name_hi": "रिकॉर्ड दुरुस्ती एवं नाम सुधार", "icon": "fa-edit"},
    {"id": "govt_land", "name": "Government & Gram Sabha Land", "name_hi": "सरकारी एवं ग्राम सभा भूमि", "icon": "fa-landmark"},
    {"id": "digital_records", "name": "Digital Portals & Bhu-Aadhaar", "name_hi": "डिजिटल पोर्टल एवं भू-आधार", "icon": "fa-laptop-code"},
    {"id": "registration", "name": "Registration & Stamp Duty", "name_hi": "रजिस्ट्री एवं स्टाम्प शुल्क", "icon": "fa-stamp"},
    {"id": "loans_mortgage", "name": "Loans & Mortgages", "name_hi": "ऋण, बंधक एवं भार मुक्ति", "icon": "fa-university"},
    {"id": "agricultural", "name": "Agricultural Land & Conversion", "name_hi": "कृषि भूमि एवं धारा 80/143", "icon": "fa-seedling"},
    {"id": "citizen_help", "name": "Citizen Help & Patwari", "name_hi": "नागरिक सहायता एवं पटवारी", "icon": "fa-headset"},
]

for cat_meta in FAQ_CATEGORIES:
    cat_meta["count"] = len(FAQS_BY_CATEGORY.get(cat_meta["id"], []))

POPULAR_FAQS = [
    "faq-own-01",  # Check land ownership
    "faq-own-02",  # Verify seller before buying
    "faq-rec-02",  # What is Khasra number
    "faq-rec-03",  # Khata vs Khasra
    "faq-rec-04",  # What is Khatauni
    "faq-rec-05",  # What is 7/12 Satbara
    "faq-mut-01",  # What is mutation (Dakhil Kharij)
    "faq-mut-02",  # How to apply for mutation
    "faq-buy-01",  # Documents to check before buying land
    "faq-buy-02",  # What is Encumbrance Certificate (EC)
    "faq-inh-01",  # Transfer after death of owner
    "faq-inh-03",  # Daughters share in ancestral land
    "faq-mea-02",  # Bigha to Acre and Hectare
    "faq-mea-06",  # Land demarcation (Seemankan)
    "faq-disp-02", # Illegal occupation / encroachment
    "faq-cor-01",  # Misspelled name in Khatauni
    "faq-loan-02", # Check if land is mortgaged to bank
    "faq-agr-01"   # Agricultural to Non-Agricultural conversion
]

# Vocabulary synonym mappings for colloquial, Hindi, and regional revenue terms
SYNONYM_MAP = {
    "namantaran": ["mutation", "dakhil", "kharij", "transfer"],
    "dakhil": ["mutation", "dakhil-kharij", "transfer"],
    "kharij": ["mutation", "dakhil-kharij"],
    "ferfar": ["mutation", "maharashtra", "7/12"],
    "inteqal": ["mutation", "punjab", "haryana"],
    "virasat": ["inheritance", "succession", "legal heir", "death"],
    "varisatan": ["inheritance", "succession", "heir"],
    "waris": ["inheritance", "legal heir"],
    "batwara": ["partition", "co-sharer", "division", "share"],
    "seemankan": ["demarcation", "boundary", "section 24"],
    "hadbandi": ["demarcation", "boundary", "pillar"],
    "paimayish": ["measurement", "demarcation", "ets"],
    "kabza": ["encroachment", "possession", "illegal", "dispute"],
    "qabza": ["encroachment", "possession", "illegal"],
    "vivad": ["dispute", "litigation", "court"],
    "med": ["boundary", "demarcation", "border"],
    "girvi": ["mortgage", "loan", "bank"],
    "gehan": ["mortgage", "loan", "bank"],
    "karz": ["loan", "bank", "kcc"],
    "shuddhata": ["correction", "rectification", "spelling", "error"],
    "sudhar": ["correction", "rectification", "name correction", "error"],
    "durusti": ["correction", "rectification", "order"],
    "galat": ["wrong", "correction", "mistake", "error"],
    "wrong": ["correction", "mistake", "error"],
    "mistake": ["correction", "spelling", "rectification"],
    "dhoka": ["fraud", "duplicate registry", "dispute"],
    "fraud": ["fraud", "dispute", "duplicate"],
    "satbara": ["7/12", "satbara", "record of rights", "maharashtra"],
    "pahani": ["pahani", "karnataka", "rtc", "record of rights"],
    "bigha": ["bigha", "measurement", "conversion", "acre"],
    "biswa": ["biswa", "bigha", "measurement"],
    "guntha": ["guntha", "measurement", "conversion", "acre"],
    "kanal": ["kanal", "marla", "measurement"],
    "marla": ["kanal", "marla", "measurement"],
    "dharani": ["dharani", "telangana", "portal"],
    "bhoomi": ["bhoomi", "karnataka", "portal"],
    "bhulekh": ["bhulekh", "up", "portal"],
    "lekhpal": ["patwari", "revenue officer", "tehsil"],
    "patwari": ["patwari", "revenue officer", "talathi"],
    "talathi": ["talathi", "patwari", "maharashtra"],
    "karnam": ["karnam", "village officer", "patwari"],
    "tehsildar": ["tehsildar", "revenue court", "officer"],
    "kanungo": ["revenue inspector", "kanungo", "patwari"],
    "sdm": ["sub-divisional magistrate", "sdm", "revenue court"],
    "daughter": ["daughters", "inheritance", "ancestral", "coparcener"],
    "daughters": ["daughter", "inheritance", "ancestral", "coparcener"],
    "women": ["female", "inheritance", "daughter"],
    "poa": ["power of attorney", "gpa", "spa"],
    "gpa": ["power of attorney", "poa", "sale"],
    "kcc": ["kisan credit card", "loan", "mortgage"],
    "fard": ["fard", "jamabandi", "punjab", "haryana"],
    "jamabandi": ["jamabandi", "fard", "record of rights"],
    "khatauni": ["khatauni", "ror", "record of rights"],
    "khasra": ["khasra", "survey number", "plot"],
    "khata": ["khata", "account", "khewat"],
    "ec": ["encumbrance certificate", "non-encumbrance", "nil encumbrance"],
}

STOPWORDS = {
    "what", "is", "are", "the", "a", "an", "for", "and", "how", "can", "tell", "show",
    "about", "with", "from", "in", "on", "of", "to", "do", "does", "did", "i", "my",
    "me", "we", "you", "he", "she", "it", "they", "please", "this", "that", "there",
    "here", "give", "help", "want", "need", "know", "check", "get", "kya", "hai", "kaise",
    "kare", "karna", "batao", "bataiye", "mera", "meri", "mere", "hoga", "chahiye"
}

def tokenize(text: str):
    """Extract lowercase alphanumeric and Devanagari word tokens, filtering common stopwords."""
    words = re.findall(r'[\w\u0900-\u097F]+', text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]

def find_matching_faq(query: str, state: str = None, category_id: str = None, min_score: float = 38.0):
    """
    Match a citizen user query against the 184 land records FAQs.
    Uses multi-signal scoring: exact phrase match, token overlap, synonym expansion,
    and query token coverage ratio.
    Returns (best_faq, score) or (None, 0).
    """
    if not query or not query.strip():
        return None, 0

    q_lower = query.strip().lower()
    raw_tokens = tokenize(q_lower)
    
    # Expand tokens with synonyms
    expanded_tokens = set(raw_tokens)
    for t in raw_tokens:
        if t in SYNONYM_MAP:
            for syn in SYNONYM_MAP[t]:
                expanded_tokens.update(tokenize(syn))
                
    best_faq = None
    best_score = 0
    
    for faq in LAND_FAQ_DATABASE:
        if category_id and faq["category_id"] != category_id:
            continue
            
        score = 0
        q_en = faq["question"].lower()
        q_hi = faq["question_hi"].lower()
        keywords = [k.lower() for k in faq.get("keywords", [])]
        state_notes = faq.get("state_notes", "").lower()
        answer = faq.get("answer", "").lower()
        
        # Token coverage calculation
        faq_all_text = (q_en + " " + q_hi + " " + " ".join(keywords) + " " + answer).lower()
        faq_all_tokens = set(tokenize(faq_all_text))
        
        if raw_tokens:
            matched_raw = [t for t in raw_tokens if t in faq_all_tokens or any(syn in faq_all_tokens for syn in SYNONYM_MAP.get(t, []))]
            coverage_ratio = len(matched_raw) / len(raw_tokens)
            score += coverage_ratio * 150
            if coverage_ratio >= 0.75:
                score += 60

        # 1. Exact phrase match
        if q_lower in q_en or (len(q_en) > 10 and q_en in q_lower):
            score += 150
        elif q_lower in q_hi or (len(q_hi) > 10 and q_hi in q_lower):
            score += 150
            
        # 2. Match exact keyword phrase
        for kw in keywords:
            if kw in q_lower:
                score += 90
            else:
                kw_words = [w for w in kw.split() if w not in STOPWORDS]
                if kw_words and sum(1 for w in kw_words if w in q_lower) >= 2:
                    score += 40
                
        # 3. Token overlap with question
        q_tokens = tokenize(q_en) + tokenize(q_hi)
        matched_tokens = expanded_tokens.intersection(set(q_tokens))
        score += len(matched_tokens) * 20
        
        # 4. Token overlap with keywords
        kw_tokens = set()
        for kw in keywords:
            kw_tokens.update(tokenize(kw))
        score += len(expanded_tokens.intersection(kw_tokens)) * 15
        
        # 5. Answer body partial match for key technical phrases
        for t in raw_tokens:
            if len(t) > 3 and t in answer:
                score += 5
                
        # 6. State match bonus
        if state and state.lower() in state_notes:
            score += 25
            
        if score > best_score:
            best_score = score
            best_faq = faq
            
    if best_score >= min_score:
        return best_faq, best_score
    return None, 0

def search_faqs(query: str = None, category_id: str = None, state: str = None, limit: int = 50):
    """
    Search and filter FAQs for the FAQ browser / modal drawer.
    Returns a list of matching FAQ objects.
    """
    results = []
    if not query or not query.strip():
        # Just filter by category or state
        for faq in LAND_FAQ_DATABASE:
            if category_id and faq["category_id"] != category_id:
                continue
            if state and state.lower() not in faq.get("state_notes", "").lower():
                continue
            results.append(faq)
            if len(results) >= limit:
                break
        return results

    scored_faqs = []
    for faq in LAND_FAQ_DATABASE:
        if category_id and faq["category_id"] != category_id:
            continue
        # Score individual FAQ
        q_tokens = tokenize(query.strip().lower())
        faq_text = (faq["question"] + " " + faq["question_hi"] + " " + " ".join(faq["keywords"])).lower()
        score = sum(1 for t in q_tokens if t in faq_text)
        if query.strip().lower() in faq_text:
            score += 10
        if score > 0:
            scored_faqs.append((score, faq))
            
    scored_faqs.sort(key=lambda x: x[0], reverse=True)
    return [faq for score, faq in scored_faqs[:limit]]

