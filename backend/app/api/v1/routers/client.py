from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Annotated, List
from ..dependencies.auth import get_current_user
from ..dependencies.get_404 import get_client_or_404

from app import models
from app.schemas import client, user
from app.service.crud import userservice, clientservice
from app.service import passwordservice

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("", status_code=status.HTTP_201_CREATED, response_model= client.ClientOut)
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

    return client_create

@router.put("/update_info/{makh}", status_code=status.HTTP_204_NO_CONTENT)
async def update_information_client(employee_role: user_dependency, db: db_dependency, client_update: client.ClientUpdate, client_get: models.Client = Depends(get_client_or_404)):
    if employee_role is None or employee_role.get('role') != "employee":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')



    id = client_get.owner_id
    user_update_info = userservice.update(db_session=db, user_change=client_update.users, id=id)
    client_update_info = clientservice.update(db_session=db,
                                              client_update=client_update.client,
                                              makh=client_get.makh)

    return client_update_info

@router.put("/change_password", status_code=status.HTTP_200_OK)
async def change_password(db: db_dependency, user: user_dependency, user_change: user.UserUpdate):
    return userservice.update_password(db_session=db, user_in=user, user_change=user_change)