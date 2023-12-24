from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from .event import EventOutOfDetail


# Shared properties
class ContractBase(BaseModel):
    mahopdong: Optional[str] = None
    giaidoan: Optional[int]
    phithanhtoan: Optional[int]
    pt_thanhtoan: Optional[str] = None
    ngaytttheohd: Optional[date]
    ngayttthucte: Optional[date]


class ContractCreate(ContractBase):
    motaphi: Optional[str] = None
    owner: Optional[str]

    class Config:
        from_attributes = True

class ContractInDB(ContractBase):
    phithanhtoan: str


class ContractUpdate(BaseModel):
    giaidoan: int
    phithanhtoan: int
    pt_thanhtoan: str
    ngaytttheohd: date
    ngayttthucte: date
    motaphi: str

class ContractOut(BaseModel):
    mahopdong: str
    giaidoan: int
    phithanhtoan: int
    ngaytttheohd: date
    ngayttthucte: date

    event: EventOutOfDetail

