from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime

class ClientModel(BaseModel):
    id: str | None = None
    name: str
    password: str  # Hashed
    phone: str
    address: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()