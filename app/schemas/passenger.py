from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
from app.models.passenger import GenderEnum

class PassengerBase(BaseModel):
    name: str
    aadhaar_card: str
    age: int
    gender: GenderEnum
    phone_no: str

class PassengerCreate(PassengerBase):
    ticket_id: str

class PassengerUpdate(BaseModel):
    name: str | None = None
    aadhaar_card: str | None = None
    age: int | None = None
    gender: GenderEnum | None = None
    phone_no: str | None = None

class PassengerOut(PassengerBase):
    id: str
    ticket_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}