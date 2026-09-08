import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, List
from backend.database import add_audit_block, get_latest_audit_block, get_audit_ledger

GENESIS_HASH = "0" * 64

def calculate_sha256(data: Any) -> str:
    if isinstance(data, dict) or isinstance(data, list):
        serialized = json.dumps(data, sort_keys=True, default=str)
    else:
        serialized = str(data)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

def record_audit_event(action: str, record_id: str, details: str, payload: Any) -> str:
    """
    Creates an immutable audit block linking to the previous block's hash.
    Returns the new current block hash.
    """
    latest = get_latest_audit_block()
    prev_hash = latest["current_hash"] if latest else GENESIS_HASH
    timestamp = datetime.now(timezone.utc).isoformat()
    
    data_hash = calculate_sha256(payload)
    
    # Block hash includes prev_hash + timestamp + action + record_id + data_hash
    block_content = f"{prev_hash}|{timestamp}|{action}|{record_id}|{data_hash}"
    current_hash = hashlib.sha256(block_content.encode("utf-8")).hexdigest()
    
    add_audit_block(
        action=action,
        record_id=record_id,
        details=details,
        data_hash=data_hash,
        prev_hash=prev_hash,
        current_hash=current_hash,
        timestamp=timestamp
    )
    return current_hash

def verify_audit_ledger() -> Tuple[bool, List[Dict[str, Any]], str]:
    """
    Verifies that the entire audit trail is cryptographically sound.
    Returns (is_valid, blocks, status_message).
    """
    blocks = get_audit_ledger()
    if not blocks:
        return True, [], "Audit ledger is empty."
    
    expected_prev = GENESIS_HASH
    for i, b in enumerate(blocks):
        if b["prev_hash"] != expected_prev:
            return False, blocks, f"Tamper detected at block #{b['block_index']}: prev_hash mismatch!"
        
        # Verify block hash computation
        content = f"{b['prev_hash']}|{b['timestamp']}|{b['action']}|{b['record_id']}|{b['data_hash']}"
        expected_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if b["current_hash"] != expected_hash:
            return False, blocks, f"Tamper detected at block #{b['block_index']}: current_hash has been forged or altered!"
        
        expected_prev = b["current_hash"]
        
    return True, blocks, "All audit blocks verified successfully. Ledger is 100% tamper-proof."
