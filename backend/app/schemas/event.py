from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from .client import ClientOutEvent


# Shared properties
class EventBase(BaseModel):
    mact: Optional[str] = None
    name: Optional[str] = None
    ngaybatdau: Optional[date]
    ngayketthuc: Optional[date]


class EventCreate(EventBase):
    owner: Optional[str] = "KH0001"

    class Config:
        from_attributes = True

class EventInDB(EventBase):
    detail: str

class EventUpdate(BaseModel):
    name: str
    ngaybatdau: date
    ngayketthuc: date
    detail: str

class EventOut(BaseModel):
    mact: str
    name: str
    ngaybatdau: date
    ngayketthuc: date
    owner_event: ClientOutEvent
