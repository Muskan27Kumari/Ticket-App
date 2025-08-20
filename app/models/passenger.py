from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"

class PassengerModel(BaseModel):
    id: str | None = None
    name: str
    aadhaar_card: str
    age: int
    gender: GenderEnum
    phone_no: str
    ticket_id: str # Reference to ticket
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()