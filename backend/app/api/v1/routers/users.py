from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import status


from app.schemas.user import UserOut, UserUpdate
from app.database import get_db
from app.service import userservice
from app import models

from ..dependencies.auth import get_current_user
from ..dependencies.get_404 import get_user_or_404

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/information", status_code= status.HTTP_200_OK, response_model=UserOut)
async def get_info_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    user_get = userservice.get(db_session=db, id_=user.get('id'))
    return user_get


@router.get("/all_user", status_code=status.HTTP_200_OK, response_model=List[UserOut])
async def get_all_user(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    all_user = userservice.get_multiple(db_session=db)
    return all_user


@router.get("/{id}", response_model=UserOut)
def get_user_by_id(user: user_dependency,user_get: models.User = Depends(get_user_or_404),):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    """
    Retrieve details about a specific user.
    """
    return user_get


@router.put("/change_password}", status_code=status.HTTP_200_OK)
async def change_password(user_change: UserUpdate, user: user_dependency, db: db_dependency):
    return userservice.update(db_session=db, user_in=user, user_change=user_change)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(user: user_dependency, db_session: db_dependency, user_delete: models.User = Depends(get_user_or_404) ):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You don't have enough authentication")

    """
       Delete an individual user.
    """

    return userservice.delete(db_session=db_session, id_=user_delete.id)