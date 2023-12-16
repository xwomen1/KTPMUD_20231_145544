from pydantic import BaseModel
from typing import Union, Optional
from .user import UserBase, UserOut, UserUpdateInfo
class ClientBase(BaseModel):
    makh: Optional[str] = "KH0001"
    address: Optional[str]
    # owner_id: int

class ClientUpdateInfo(BaseModel):
    address: str


class ClientCreate(BaseModel):
    users: UserBase
    client: ClientBase

class ClientUpdate(BaseModel):
    users: UserUpdateInfo
    client: ClientUpdateInfo

class ClientOut(BaseModel):
    makh: str
    owner: UserOut

class ClientOutEvent(BaseModel):
    makh: str
    address: str
