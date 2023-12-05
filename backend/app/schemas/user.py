from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = True

class UserOut(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    role: Optional[str] = None

class UserCreate(UserBase):
    username: str
    password: str

class UserUpdate(BaseModel):
    password: str
    new_password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str