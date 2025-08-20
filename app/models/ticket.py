from bson import ObjectId
from pydantic import BaseModel
from datetime import datetime

class TicketModel(BaseModel):
    id: str | None = None
    from_location: str
    to_location: str
    price: float
    date_of_journey: datetime
    passengers: list[str] = []  # References to passenger IDs
    user_id: str  # Reference to user
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()