from fastapi import APIRouter, Depends, HTTPException, status

from typing import Annotated, List
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import employee
from app.service.crud import userservice, employeeservice
from app.service import passwordservice
from app import models
from ..dependencies.auth import get_current_user
from ..dependencies.get_404 import get_employee_or_404
router = APIRouter()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("", status_code=status.HTTP_201_CREATED, response_model=employee.Employee)
async def create_employee(db: db_dependency, create_employee_request: employee.EmployeeCreate):
    # hash the password - user.password
    hashed_password = passwordservice.get_password_hash(create_employee_request.users.password)
    create_employee_request.users.password = hashed_password

    if userservice.get_by_email(db_session=db, email=create_employee_request.users.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already exists",
        )

    if userservice.get_by_username(db_session=db, username=create_employee_request.users.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username already exists",
        )
    if userservice.get_by_phonenumber(db_session=db, phonenumber=create_employee_request.users.phonenumber):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="phonenumber already exists",
        )

    user = await userservice.create(db_session=db, user_in=create_employee_request.users)
    employee_create = employeeservice.create(db_session=db, employee_in=create_employee_request.employee, owner_id_get=user.id)

    return employee_create

@router.get("/information/{manv}", status_code= status.HTTP_200_OK)
def get_employee_by_manv(employee_get: models.Employee = Depends(get_employee_or_404)):
    """
    Retrieve details about a specific employee.
    """
    return employee_get

@router.get("/all_employee", status_code=status.HTTP_200_OK,response_model=List[employee.Employee])
async def get_all_employee(db: db_dependency):
    all_employee = employeeservice.get_multiple(db_session=db)
    return all_employee

@router.put("/update_info/{manv}", status_code=status.HTTP_204_NO_CONTENT)
async def update_information_employee(db: db_dependency, employee_update: employee.EmployeeUpdate, employee_get_manv: models.Employee = Depends(get_employee_or_404)):
    id = employee_get_manv.owner_id
    user_update_info = userservice.update(db_session=db,user_change=employee_update.users, id=id)
    employee_update_info = employeeservice.update(db_session=db,employee_update=employee_update.employee, manv=employee_get_manv.manv)

    return employee_update_info
@router.delete("/{manv}", status_code=status.HTTP_200_OK)
async def delete_employee(db: db_dependency, employee_delete: models.Employee = Depends(get_employee_or_404)):
    """
       Delete an individual employee.
    """
    return employeeservice.delete(db_session=db, manv=employee_delete.manv)