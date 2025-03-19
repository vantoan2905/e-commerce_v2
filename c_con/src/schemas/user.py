from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    phone_number: str
    name: str
    role: str
    created_at: datetime

class UserUpdate(UserBase):
    id : int
    username: str
    email: EmailStr
    password: str
    phone_number: str
    name: str
    role: str
    created_at: datetime

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
