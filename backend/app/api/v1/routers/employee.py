from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Annotated, List
from ..dependencies.auth import get_current_user
from app import models
from app.schemas import client, user, employee
from app.service.crud import userservice, clientservice
from app.service import passwordservice
from ..dependencies.get_404 import get_client_or_404

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/information/{makh}", status_code= status.HTTP_200_OK, response_model= client.ClientOut)
def get_client_by_makh(employee_role: user_dependency, client_get: models.Client = Depends(get_client_or_404)):
    if employee_role is None or employee_role.get('role') != "employee":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    """
    Retrieve details about a specific client.
    """
    return client_get


@router.get("/all_client", status_code=status.HTTP_200_OK,response_model=List[client.ClientOut])
async def get_all_client(employee_role: user_dependency, db: db_dependency):
    if employee_role is None or employee_role.get('role') != "employee":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    all_client = clientservice.get_multiple(db_session=db)
    return all_client

@router.put("/change_password", status_code=status.HTTP_200_OK)
async def change_password(db: db_dependency, user: user_dependency, user_change: user.UserUpdate):
    return userservice.update_password(db_session=db, user_in=user, user_change=user_change)



@router.delete("/{makh}", status_code=status.HTTP_200_OK)
async def delete_client(employee_role: user_dependency, db: db_dependency, client_delete: models.Client = Depends(get_client_or_404)):
    if employee_role is None or employee_role.get('role') != "employee":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    """
       Delete an individual client.
    """
    return clientservice.delete(db_session=db, makh=client_delete.makh)

