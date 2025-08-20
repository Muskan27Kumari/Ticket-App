from bson import ObjectId
from pydantic import BaseModel
from datetime import datetime

class UserModel(BaseModel):
    id: str | None = None
    name: str
    email: str
    password: str  # Hashed
    phone: str
    tickets: list[str] = []  # References to ticket IDs
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()