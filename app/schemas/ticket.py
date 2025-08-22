from pydantic import BaseModel
from bson import ObjectId
from typing import List
from datetime import datetime

class TicketBase(BaseModel):
    from_location: str
    to_location: str
    price: float
    date_of_journey: datetime

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    from_location: str | None = None
    to_location: str | None = None
    price: float | None = None
    date_of_journey: datetime | None = None

class TicketOut(TicketBase):
    id: str
    user_id: str
    passengers: List[str] = []  # Passenger IDs as strings
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}