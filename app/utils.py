from bson import ObjectId
from datetime import datetime
from typing import Any, Dict, Tuple
import re
# app/utils/token_blacklist.py


def convert_objectid_to_str(data: Any) -> Any:
    """
    Recursively convert ObjectId to str in dicts or lists.
    """
    if isinstance(data, dict):
        return {k: convert_objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(i) for i in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

def get_current_utc() -> datetime:
    """
    Get current UTC datetime.
    """
    return datetime.utcnow()

def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate password strength.
    Returns (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    return True, ""