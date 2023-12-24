from fastapi import APIRouter, status, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import contract
from app.service.crud import contractservice
from app.exceptions import apiexceptions

from ..dependencies.auth import get_current_user
from ..dependencies.get_404 import get_contract_or_404

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("", status_code=status.HTTP_201_CREATED, response_model=contract.ContractOut)
async def create_contract(db: db_dependency, employee_role: user_dependency, contract_create: contract.ContractCreate):
    if employee_role is None or employee_role.get('role') != "employee":
        raise apiexceptions.InvalidCredentialsException
    return contractservice.create(db_session=db,contract=contract_create)

@router.get("/{mahopdong}", status_code=status.HTTP_200_OK, response_model=contract.ContractOut)
def get_contract(employee_role: user_dependency, contract_get: models.HopDong = Depends(get_contract_or_404)):
    if employee_role is None or employee_role.get('role') != "employee":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    return contract_get





@router.put("/update/{mahopdong}", status_code=status.HTTP_204_NO_CONTENT)
async def update_contract(db: db_dependency,
                    employee_role: user_dependency,
                    contract_update: contract.ContractUpdate,
                    contract_get :models.HopDong= Depends(get_contract_or_404)
                    ):

    if employee_role is None or employee_role.get('role') != "employee":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')



    return contractservice.update(db_session=db, contract_update=contract_update, mahopdong=contract_get.mahopdong)

@router.delete("/{mahopdong}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contract(db: db_dependency,
                    employee_role: user_dependency,
                    contract_get: models.HopDong = Depends(get_contract_or_404)):
    if employee_role is None or employee_role.get('role') != "employee":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    return contractservice.delete(db_session=db, mahopdong=contract_get.mahopdong)

