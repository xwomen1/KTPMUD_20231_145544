from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None

class UserCreate(BaseModel):
    email: Optional[EmailStr] = None
    password: str
    role: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    role: str

    class Config:
        from_attributes = True
