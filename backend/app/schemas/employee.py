from pydantic import BaseModel
from typing import Optional
from datetime import date
from .user import UserOut, UserBase
class EmployeeBase(BaseModel):
    manv: str
    salary: Optional[int]
    ngaybatdaucongtac: date
    ngayketthuccongtac: date
    # owner_id: int

    # owner: UserOut

class EmployeeOut(BaseModel):
    manv: str
    owner: UserOut

class EmployeeCreate(BaseModel):
    users: UserBase
    employee: EmployeeBase
