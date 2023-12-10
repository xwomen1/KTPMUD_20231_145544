from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import timedelta

from app.config import settings
from app.database import get_db
from app.schemas import employee, token
from app.service import userservice, employeeservice
from ..dependencies.auth import create_access_token, authenticate_user

router = APIRouter()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: employee.EmployeeCreate):
    if userservice.get_by_email(db_session=db, email=create_user_request.users.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already exists",
        )

    user = await userservice.create(db_session=db, user_in=create_user_request.users)
    employee_create = employeeservice.create(db_session=db, employee_in=create_user_request.employee, owner_id_get=user.id)

    return {"email": user.email, "fullname": user.fullname, "manv": employee_create.manv}


@router.post("/login", response_model= token.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    db.commit()
    token = create_access_token(form_data.username, user.id, user.role, timedelta(minutes=settings.access_token_expire_minutes))

    return {'access_token': token, 'token_type': 'bearer'}

@router.post("/logout")
def logout():
    return {"logout-status": "successful"}
