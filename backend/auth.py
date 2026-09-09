import os
import hmac
import hashlib
import secrets
import json
import base64
import time
import re
from typing import Optional, Tuple, Dict, Any
from fastapi import Header, HTTPException, status

# Cryptographic Configuration
SECRET_KEY = os.environ.get("AUTH_SECRET_KEY", "bhoomi-dilrmp-national-cadastral-security-key-2026-sha256")
PBKDF2_ITERATIONS = 100000
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def validate_email_format(email: str) -> bool:
    """Validates if the provided string is a valid email address."""
    if not email or not isinstance(email, str):
        return False
    email = email.strip()
    if len(email) < 5 or len(email) > 254:
        return False
    return bool(EMAIL_REGEX.match(email))

def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """
    Hashes a password using NIST SP 800-132 PBKDF2-HMAC-SHA256 with 100,000 iterations.
    Returns (hash_hex, salt_hex).
    """
    if not salt:
        salt = secrets.token_hex(16)
    
    salt_bytes = bytes.fromhex(salt)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt_bytes,
        PBKDF2_ITERATIONS
    )
    return key.hex(), salt

def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    """
    Verifies a password against the stored salt and expected hash using
    constant-time comparison to protect against timing attacks.
    """
    try:
        computed_hash, _ = hash_password(password, salt)
        return hmac.compare_digest(computed_hash, expected_hash)
    except Exception:
        return False

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def _b64url_decode(s: str) -> bytes:
    padding = '=' * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + padding)

def create_access_token(user_id: str, email: str, role: str, expires_in_hours: int = 72) -> str:
    """
    Generates a cryptographically signed URL-safe access token (HMAC-SHA256).
    """
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": user_id,
        "email": email.strip().lower(),
        "role": role,
        "exp": int(time.time()) + (expires_in_hours * 3600),
        "iat": int(time.time()),
        "jti": secrets.token_hex(8)
    }
    
    header_b64 = _b64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))
    
    signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    signature = hmac.new(SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
    sig_b64 = _b64url_encode(signature)
    
    return f"{header_b64}.{payload_b64}.{sig_b64}"

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes and cryptographically verifies an access token.
    Returns payload dictionary if valid and unexpired; None otherwise.
    """
    if not token or not isinstance(token, str):
        return None
    
    parts = token.strip().split('.')
    if len(parts) != 3:
        return None
    
    header_b64, payload_b64, sig_b64 = parts
    try:
        signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
        expected_sig = hmac.new(SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
        provided_sig = _b64url_decode(sig_b64)
        
        if not hmac.compare_digest(expected_sig, provided_sig):
            return None
        
        payload_bytes = _b64url_decode(payload_b64)
        payload = json.loads(payload_bytes.decode('utf-8'))
        
        # Check expiry
        if int(payload.get("exp", 0)) < int(time.time()):
            return None
        
        return payload
    except Exception:
        return None

def extract_token_from_header(authorization: Optional[str]) -> Optional[str]:
    """Extracts bearer token from Authorization header value."""
    if not authorization:
        return None
    parts = authorization.strip().split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    if len(parts) == 1:
        return parts[0]
    return None

def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    """
    Optional authentication dependency. Returns user payload dict if valid token supplied,
    or None if no header or invalid token.
    """
    token = extract_token_from_header(authorization)
    if not token:
        return None
    return decode_access_token(token)

def get_current_user_required(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    Enforced authentication dependency. Raises HTTP 401 if missing or invalid token.
    """
    user = get_current_user_optional(authorization)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
