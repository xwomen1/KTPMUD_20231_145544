from pydantic import BaseModel
from typing import Union, Optional
from .user import UserBase, UserOut
class ClientBase(BaseModel):
    makh: str = "KH0001"
    address: Optional[str]
    # owner_id: int

class ClientCreate(BaseModel):
    users: UserBase
    client: ClientBase

class ClientOut(BaseModel):
    makh: str
    owner: UserOut
