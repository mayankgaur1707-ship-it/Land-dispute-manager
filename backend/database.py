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
        updated_at TEXT NOT NULL
    )
    """)
    
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

def save_record(record_dict: Dict[str, Any]):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO records (
        id, khasra_no, khata_no, village, tehsil, district, state,
        area_sq_meters, area_hectares, area_acres, land_type,
        owners_json, boundary_geojson, dispute_status, dispute_tags_json,
        confidence_score, document_source, audit_hash, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        json.dumps(record_dict["owners"]),
        json.dumps(record_dict["boundary_geojson"]),
        record_dict["dispute_status"],
        json.dumps(record_dict.get("dispute_tags", [])),
        record_dict["confidence_score"],
        record_dict.get("document_source", ""),
        record_dict["audit_hash"],
        record_dict["created_at"],
        record_dict["updated_at"]
    ))
    conn.commit()
    conn.close()

def get_all_records() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records ORDER BY created_at DESC")
    rows = cursor.fetchall()
    records = []
    for row in rows:
        rec = dict(row)
        rec["owners"] = json.loads(rec["owners_json"])
        rec["boundary_geojson"] = json.loads(rec["boundary_geojson"])
        rec["dispute_tags"] = json.loads(rec["dispute_tags_json"])
        del rec["owners_json"]
        del rec["dispute_tags_json"]
        records.append(rec)
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
    rec = dict(row)
    rec["owners"] = json.loads(rec["owners_json"])
    rec["boundary_geojson"] = json.loads(rec["boundary_geojson"])
    rec["dispute_tags"] = json.loads(rec["dispute_tags_json"])
    del rec["owners_json"]
    del rec["dispute_tags_json"]
    return rec

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
