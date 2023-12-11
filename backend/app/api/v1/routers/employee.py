from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Annotated, List
from ..dependencies.auth import get_current_user

from app.schemas import client
from app.service.crud import userservice, clientservice
from app.service import passwordservice

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_client(db: db_dependency, employee_role: user_dependency, create_client_request: client.ClientCreate):
    if employee_role is None or employee_role.get('role') != "employee":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    # hash the password - user.password
    hashed_password = passwordservice.get_password_hash(create_client_request.users.password)
    create_client_request.users.password = hashed_password

    if userservice.get_by_email(db_session=db, email=create_client_request.users.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already exists",
        )

    if userservice.get_by_username(db_session=db, username=create_client_request.users.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username already exists",
        )
    if userservice.get_by_phonenumber(db_session=db, phonenumber=create_client_request.users.phonenumber):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="phonenumber already exists",
        )

    user = await userservice.create(db_session=db, user_in=create_client_request.users)
    client_create = clientservice.create(db_session=db, client_in=create_client_request.client, owner_id_get=user.id)

    return {"email": user.email, "fullname": user.fullname, "makh": client_create.makh}