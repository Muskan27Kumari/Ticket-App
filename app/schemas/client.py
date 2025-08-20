from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    phone: str
    address: str

class ClientCreate(ClientBase):
    password: str

class ClientUpdate(BaseModel):
    phone: str | None = None
    address: str | None = None
    password: str | None = None

class ClientOut(ClientBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}