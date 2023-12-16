from pydantic import BaseModel
from typing import Optional
from datetime import date
from .user import UserOut, UserBase, UserUpdateInfo
class EmployeeBase(BaseModel):
    manv: str = "NV0001"
    salary: Optional[int]
    ngaybatdaucongtac: date
    ngayketthuccongtac: date
    # owner_id: int

    # owner: UserOut

class EmployeeUpdateInfo(BaseModel):
    salary: Optional[int]
    ngaybatdaucongtac: date
    ngayketthuccongtac: date



class Employee(BaseModel):
    manv: str
    salary: int
    ngaybatdaucongtac: date
    ngayketthuccongtac: date

    owner: UserOut
    class Config:
        from_attributes = True

class EmployeeOut(EmployeeBase):
    pass

class EmployeeCreate(BaseModel):
    users: UserBase
    employee: EmployeeBase

class EmployeeUpdate(BaseModel):
    users: UserUpdateInfo
    employee: EmployeeUpdateInfo
