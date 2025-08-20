from pydantic import BaseModel, EmailStr
from bson import ObjectId
from typing import List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    password: str | None = None

class UserOut(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    tickets: List[str] = []  # Ticket IDs as strings

    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}