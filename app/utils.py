from bson import ObjectId
from datetime import datetime
from typing import Any, Dict
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