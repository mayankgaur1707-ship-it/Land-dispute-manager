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

class Owner(BaseModel):
    name: str
    aadhaar_masked: Optional[str] = "XXXX-XXXX-1234"
    share_percentage: float = 100.0  # Percentage ownership e.g. 50.0, 100.0
    father_or_husband_name: Optional[str] = None
    contact: Optional[str] = None

class LandRecordBase(BaseModel):
    khasra_no: str  # Survey / Khasra number
    khata_no: str   # Khata / Account number
    village: str
    tehsil: str
    district: str
    state: str
    area_sq_meters: float
    land_type: LandClassification = LandClassification.AGRICULTURAL
    owners: List[Owner]
    boundary_geojson: Dict[str, Any]  # GeoJSON Polygon: {"type": "Polygon", "coordinates": [...]}
    document_source: Optional[str] = "Scanned Revenue Deed"

class LandRecordCreate(LandRecordBase):
    pass

class LandRecord(LandRecordBase):
    id: str
    area_hectares: float
    area_acres: float
    dispute_status: DisputeStatus = DisputeStatus.CLEAR
    dispute_tags: List[str] = []
    confidence_score: float = 1.0  # OCR / Data extraction confidence (0.0 - 1.0)
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
    severity: str = "HIGH"  # LOW, MEDIUM, HIGH, CRITICAL
    status: str = "ACTIVE"  # ACTIVE, RESOLVED, DISMISSED
    resolution_notes: Optional[str] = None
    created_at: str
    resolved_at: Optional[str] = None

class MutationRequest(BaseModel):
    record_id: str
    new_owners: List[Owner]
    transfer_type: str = "SALE_DEED"  # SALE_DEED, INHERITANCE, GIFT, PARTITION
    deed_number: str
    remarks: Optional[str] = None

class AuditBlock(BaseModel):
    index: int
    timestamp: str
    action: str
    record_id: str
    details: str
    data_hash: str
    prev_hash: str
    current_hash: str
