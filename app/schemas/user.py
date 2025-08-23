from pydantic import BaseModel, EmailStr, validator
from bson import ObjectId
from typing import List
from datetime import datetime
from app.utils import validate_password

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password_strength(cls, v):
        is_valid, error_message = validate_password(v)
        if not is_valid:
            raise ValueError(error_message)
        return v

class UserUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    password: str | None = None
    
    @validator('password')
    def validate_password_strength(cls, v):
        if v is not None:  # Only validate if password is provided
            is_valid, error_message = validate_password(v)
            if not is_valid:
                raise ValueError(error_message)
        return v

class UserOut(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    tickets: List[str] = []  # Ticket IDs as strings

    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}