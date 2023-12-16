from fastapi import APIRouter, status, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session


from app.database import get_db
from app import models
from app.schemas import event
from app.service.crud import eventservice

from ..dependencies.auth import get_current_user
from ..dependencies.get_404 import get_event_or_404

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
@router.post("", status_code= status.HTTP_201_CREATED, response_model=event.EventOut)
async def create_event(employee_role: user_dependency, db: db_dependency, create_event_request: event.EventCreate):
    if employee_role is None or employee_role.get('role') != "employee":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    event = eventservice.create(db_session=db, event=create_event_request)
    return event


@router.get("/information/{mact}", status_code= status.HTTP_200_OK, response_model= event.EventOut)
def get_event_by_mact(employee_role: user_dependency, event_get: models.Event = Depends(get_event_or_404)):
    if employee_role is None or employee_role.get('role') != "employee":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    """
    Retrieve about an event.
    """
    return event_get


@router.get("/all_event", status_code=status.HTTP_200_OK, response_model=event.EventOut)
async def get_all_event(employee_role: user_dependency, db: db_dependency):
    if employee_role is None or employee_role.get('role') != "employee":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    all_event = eventservice.get_multiple(db_session=db)

    return all_event


@router.put("/{mact}", status_code=status.HTTP_204_NO_CONTENT)
async def update_event(employee_role: user_dependency, db: db_dependency, event_update: event.EventUpdate, event_get: models.Event = Depends(get_event_or_404)):
    if employee_role is None or employee_role.get('role') != "employee":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')


    """
        Update an individual event.
    """

    return eventservice.update(db_session=db, event_update=event_update, mact=event_get.mact)

@router.delete("/{mact}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(employee_role: user_dependency, db: db_dependency, event_get: models.Event = Depends(get_event_or_404)):
    if employee_role is None or employee_role.get('role') != "employee":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    """
        Delete an individual event.
    """
    return eventservice.delete(db_session=db, mact=event_get.mact)

