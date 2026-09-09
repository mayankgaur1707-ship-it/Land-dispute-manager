import sqlite3
import json
import os
from typing import List, Optional, Dict, Any

DB_PATH = os.environ.get("LAND_DB_PATH", "land_records.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id TEXT PRIMARY KEY,
        khasra_no TEXT NOT NULL,
        khata_no TEXT NOT NULL,
        village TEXT NOT NULL,
        tehsil TEXT NOT NULL,
        district TEXT NOT NULL,
        state TEXT NOT NULL,
        area_sq_meters REAL NOT NULL,
        area_hectares REAL NOT NULL,
        area_acres REAL NOT NULL,
        land_type TEXT NOT NULL,
        owners_json TEXT NOT NULL,
        boundary_geojson TEXT NOT NULL,
        dispute_status TEXT NOT NULL,
        dispute_tags_json TEXT NOT NULL,
        confidence_score REAL NOT NULL,
        document_source TEXT,
        audit_hash TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        language TEXT DEFAULT 'Hindi (हिंदी)',
        document_type TEXT DEFAULT 'Scanned PDF / Khasra',
        verification_status TEXT DEFAULT 'AUTO_VERIFIED',
        verified_by TEXT,
        verified_at TEXT,
        field_confidences_json TEXT DEFAULT '{}',
        dilrmp_cross_verified INTEGER DEFAULT 1,
        mutation_no TEXT,
        registration_date TEXT,
        correction_history_json TEXT DEFAULT '[]'
    )
    """)

    # Automatic schema migration for existing sqlite db
    cursor.execute("PRAGMA table_info(records)")
    columns = [col[1] for col in cursor.fetchall()]
    
    migrations = [
        ("language", "TEXT DEFAULT 'Hindi (हिंदी)'"),
        ("document_type", "TEXT DEFAULT 'Scanned PDF / Khasra'"),
        ("verification_status", "TEXT DEFAULT 'AUTO_VERIFIED'"),
        ("verified_by", "TEXT"),
        ("verified_at", "TEXT"),
        ("field_confidences_json", "TEXT DEFAULT '{}'"),
        ("dilrmp_cross_verified", "INTEGER DEFAULT 1"),
        ("mutation_no", "TEXT"),
        ("registration_date", "TEXT"),
        ("correction_history_json", "TEXT DEFAULT '[]'")
    ]
    for col_name, col_type in migrations:
        if col_name not in columns:
            try:
                cursor.execute(f"ALTER TABLE records ADD COLUMN {col_name} {col_type}")
            except Exception:
                pass
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disputes (
        id TEXT PRIMARY KEY,
        record_ids_json TEXT NOT NULL,
        dispute_type TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        overlap_geojson TEXT,
        overlap_area_sq_meters REAL,
        severity TEXT NOT NULL,
        status TEXT NOT NULL,
        resolution_notes TEXT,
        created_at TEXT NOT NULL,
        resolved_at TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_ledger (
        block_index INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        action TEXT NOT NULL,
        record_id TEXT NOT NULL,
        details TEXT NOT NULL,
        data_hash TEXT NOT NULL,
        prev_hash TEXT NOT NULL,
        current_hash TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

def _deserialize_record(row: sqlite3.Row) -> Dict[str, Any]:
    rec = dict(row)
    rec["owners"] = json.loads(rec.get("owners_json") or "[]")
    rec["boundary_geojson"] = json.loads(rec.get("boundary_geojson") or "{}")
    rec["dispute_tags"] = json.loads(rec.get("dispute_tags_json") or "[]")
    rec["field_confidences"] = json.loads(rec.get("field_confidences_json") or "{}")
    rec["correction_history"] = json.loads(rec.get("correction_history_json") or "[]")
    rec["dilrmp_cross_verified"] = bool(rec.get("dilrmp_cross_verified", 1))

    for k in ["owners_json", "dispute_tags_json", "field_confidences_json", "correction_history_json"]:
        if k in rec:
            del rec[k]
    return rec

def save_record(record_dict: Dict[str, Any]):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO records (
        id, khasra_no, khata_no, village, tehsil, district, state,
        area_sq_meters, area_hectares, area_acres, land_type,
        owners_json, boundary_geojson, dispute_status, dispute_tags_json,
        confidence_score, document_source, audit_hash, created_at, updated_at,
        language, document_type, verification_status, verified_by, verified_at,
        field_confidences_json, dilrmp_cross_verified, mutation_no, registration_date,
        correction_history_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record_dict["id"],
        record_dict["khasra_no"],
        record_dict["khata_no"],
        record_dict["village"],
        record_dict["tehsil"],
        record_dict["district"],
        record_dict["state"],
        record_dict["area_sq_meters"],
        record_dict["area_hectares"],
        record_dict["area_acres"],
        record_dict["land_type"],
        json.dumps(record_dict.get("owners", [])),
        json.dumps(record_dict.get("boundary_geojson", {})),
        record_dict["dispute_status"],
        json.dumps(record_dict.get("dispute_tags", [])),
        record_dict.get("confidence_score", 1.0),
        record_dict.get("document_source", ""),
        record_dict["audit_hash"],
        record_dict["created_at"],
        record_dict["updated_at"],
        record_dict.get("language", "Hindi (हिंदी)"),
        record_dict.get("document_type", "Scanned PDF / Khasra"),
        record_dict.get("verification_status", "AUTO_VERIFIED"),
        record_dict.get("verified_by"),
        record_dict.get("verified_at"),
        json.dumps(record_dict.get("field_confidences", {})),
        1 if record_dict.get("dilrmp_cross_verified", True) else 0,
        record_dict.get("mutation_no"),
        record_dict.get("registration_date"),
        json.dumps(record_dict.get("correction_history", []))
    ))
    conn.commit()
    conn.close()

def get_all_records() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records ORDER BY created_at DESC")
    rows = cursor.fetchall()
    records = [_deserialize_record(row) for row in rows]
    conn.close()
    return records

def get_record_by_id(record_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return _deserialize_record(row)

def get_pending_verifications() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records WHERE verification_status = 'PENDING_VERIFICATION' ORDER BY created_at DESC")
    rows = cursor.fetchall()
    records = [_deserialize_record(row) for row in rows]
    conn.close()
    return records

def get_state_district_analytics() -> Dict[str, Any]:
    records = get_all_records()
    state_breakdown = {}
    district_breakdown = {}

    for r in records:
        st = r.get("state", "Uttar Pradesh")
        dist = f"{r.get('district', 'Varanasi')} ({st})"
        
        if st not in state_breakdown:
            state_breakdown[st] = {"total": 0, "verified": 0, "disputed": 0, "hectares": 0.0}
        state_breakdown[st]["total"] += 1
        state_breakdown[st]["hectares"] += r.get("area_hectares", 0.0)
        if r.get("dispute_status") == "CLEAR":
            state_breakdown[st]["verified"] += 1
        elif r.get("dispute_status") == "DISPUTED":
            state_breakdown[st]["disputed"] += 1

        if dist not in district_breakdown:
            district_breakdown[dist] = {"total": 0, "verified": 0, "disputed": 0, "hectares": 0.0}
        district_breakdown[dist]["total"] += 1
        district_breakdown[dist]["hectares"] += r.get("area_hectares", 0.0)
        if r.get("dispute_status") == "CLEAR":
            district_breakdown[dist]["verified"] += 1
        elif r.get("dispute_status") == "DISPUTED":
            district_breakdown[dist]["disputed"] += 1

    return {
        "states": state_breakdown,
        "districts": district_breakdown
    }


def save_dispute(dispute_dict: Dict[str, Any]):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO disputes (
        id, record_ids_json, dispute_type, title, description,
        overlap_geojson, overlap_area_sq_meters, severity, status,
        resolution_notes, created_at, resolved_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dispute_dict["id"],
        json.dumps(dispute_dict["record_ids"]),
        dispute_dict["dispute_type"],
        dispute_dict["title"],
        dispute_dict["description"],
        json.dumps(dispute_dict.get("overlap_geojson")) if dispute_dict.get("overlap_geojson") else None,
        dispute_dict.get("overlap_area_sq_meters"),
        dispute_dict["severity"],
        dispute_dict["status"],
        dispute_dict.get("resolution_notes"),
        dispute_dict["created_at"],
        dispute_dict.get("resolved_at")
    ))
    conn.commit()
    conn.close()

def get_all_disputes(status: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    if status:
        cursor.execute("SELECT * FROM disputes WHERE status = ? ORDER BY created_at DESC", (status,))
    else:
        cursor.execute("SELECT * FROM disputes ORDER BY created_at DESC")
    rows = cursor.fetchall()
    disputes = []
    for row in rows:
        d = dict(row)
        d["record_ids"] = json.loads(d["record_ids_json"])
        d["overlap_geojson"] = json.loads(d["overlap_geojson"]) if d["overlap_geojson"] else None
        del d["record_ids_json"]
        disputes.append(d)
    conn.close()
    return disputes

def update_dispute_status(dispute_id: str, status: str, notes: str, resolved_at: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE disputes 
    SET status = ?, resolution_notes = ?, resolved_at = ?
    WHERE id = ?
    """, (status, notes, resolved_at, dispute_id))
    conn.commit()
    conn.close()

def add_audit_block(action: str, record_id: str, details: str, data_hash: str, prev_hash: str, current_hash: str, timestamp: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO audit_ledger (timestamp, action, record_id, details, data_hash, prev_hash, current_hash)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, action, record_id, details, data_hash, prev_hash, current_hash))
    conn.commit()
    conn.close()

def get_audit_ledger() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_ledger ORDER BY block_index ASC")
    rows = cursor.fetchall()
    blocks = [dict(row) for row in rows]
    conn.close()
    return blocks

def get_latest_audit_block() -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_ledger ORDER BY block_index DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
