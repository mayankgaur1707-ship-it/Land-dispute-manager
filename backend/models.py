from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

class LandClassification(str, Enum):
    AGRICULTURAL = "Agricultural"
    RESIDENTIAL = "Residential"
    COMMERCIAL = "Commercial"
    INDUSTRIAL = "Industrial"
    FOREST = "Forest Land"
    GOVERNMENT = "Government/Public"

class DisputeStatus(str, Enum):
    CLEAR = "CLEAR"
    WARNING = "WARNING"
    DISPUTED = "DISPUTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    RESOLVED = "RESOLVED"

class DisputeType(str, Enum):
    NONE = "NONE"
    BOUNDARY_OVERLAP = "BOUNDARY_OVERLAP"
    DUPLICATE_SURVEY_NO = "DUPLICATE_SURVEY_NO"
    OWNERSHIP_SHARE_MISMATCH = "OWNERSHIP_SHARE_MISMATCH"
    CHAIN_OF_TITLE_BREACH = "CHAIN_OF_TITLE_BREACH"
    AREA_DISCREPANCY = "AREA_DISCREPANCY"
    CROSS_DB_MISMATCH = "CROSS_DB_MISMATCH"

class VerificationStatus(str, Enum):
    AUTO_VERIFIED = "AUTO_VERIFIED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    VERIFIED_BY_OFFICER = "VERIFIED_BY_OFFICER"
    REJECTED = "REJECTED"

class DocumentType(str, Enum):
    HANDWRITTEN_REGISTER = "Handwritten Register"
    SCANNED_PDF = "Scanned PDF / Khasra"
    PRINTED_KHATIAN = "Printed Khatian"
    CADASTRAL_MAP = "Cadastral Map"
    MUTATION_ORDER = "Mutation Order"

class SupportedLanguage(str, Enum):
    HINDI = "Hindi (हिंदी)"
    MARATHI = "Marathi (मराठी)"
    TELUGU = "Telugu (తెలుగు)"
    TAMIL = "Tamil (தமிழ்)"
    BENGALI = "Bengali (বাংলা)"
    ENGLISH = "English"

class UserRole(str, Enum):
    REVENUE_OFFICER = "REVENUE_OFFICER"  # Patwari / Tehsildar
    CITIZEN_FARMER = "CITIZEN_FARMER"    # Citizen / Landowner
    BANK_OFFICER = "BANK_OFFICER"        # Financial Institution
    DILRMP_ADMIN = "DILRMP_ADMIN"        # State / National Administrator

class FieldConfidence(BaseModel):
    value: Any
    confidence: float  # 0.0 to 1.0
    is_low_confidence: bool = False  # True if confidence < 0.85
    bounding_box: Optional[List[int]] = None  # [ymin, xmin, ymax, xmax] relative px

class Owner(BaseModel):
    name: str
    aadhaar_masked: Optional[str] = "XXXX-XXXX-1234"
    share_percentage: float = 100.0
    father_or_husband_name: Optional[str] = None
    contact: Optional[str] = None
    confidence: float = 0.95

class LandRecordBase(BaseModel):
    khasra_no: str
    khata_no: str
    village: str
    tehsil: str
    district: str
    state: str
    area_sq_meters: float
    land_type: LandClassification = LandClassification.AGRICULTURAL
    owners: List[Owner]
    boundary_geojson: Dict[str, Any]
    document_source: Optional[str] = "Scanned Revenue Deed"
    document_type: DocumentType = DocumentType.SCANNED_PDF
    language: SupportedLanguage = SupportedLanguage.HINDI
    mutation_no: Optional[str] = None
    registration_date: Optional[str] = None

class LandRecordCreate(LandRecordBase):
    pass

class LandRecord(LandRecordBase):
    id: str
    area_hectares: float
    area_acres: float
    dispute_status: DisputeStatus = DisputeStatus.CLEAR
    dispute_tags: List[str] = []
    confidence_score: float = 1.0
    field_confidences: Dict[str, FieldConfidence] = {}
    verification_status: VerificationStatus = VerificationStatus.AUTO_VERIFIED
    verified_by: Optional[str] = None
    verified_at: Optional[str] = None
    dilrmp_cross_verified: bool = False
    correction_history: List[Dict[str, Any]] = []
    audit_hash: str
    created_at: str
    updated_at: str

class DisputeRecord(BaseModel):
    id: str
    record_ids: List[str]
    dispute_type: DisputeType
    title: str
    description: str
    overlap_geojson: Optional[Dict[str, Any]] = None
    overlap_area_sq_meters: Optional[float] = None
    severity: str = "HIGH"
    status: str = "ACTIVE"
    resolution_notes: Optional[str] = None
    created_at: str
    resolved_at: Optional[str] = None

class HumanVerificationSubmission(BaseModel):
    record_id: str
    corrected_fields: Dict[str, Any]
    officer_name: str
    remarks: Optional[str] = "Field values verified against physical revenue register."

class AuditBlock(BaseModel):
    index: int
    timestamp: str
    action: str
    record_id: str
    details: str
    data_hash: str
    prev_hash: str
    current_hash: str

