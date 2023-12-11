from fastapi import APIRouter, Depends, HTTPException, status

from typing import Annotated
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import employee
from app.service.crud import userservice, employeeservice
from app.service import passwordservice

router = APIRouter()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("", status_code=status.HTTP_201_CREATED)
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

    return {"email": user.email, "fullname": user.fullname, "manv": employee_create.manv}

@router.get("/{manv}/information", status_code= status.HTTP_200_OK)
async def get_info_employee(db: db_dependency):
    return 0