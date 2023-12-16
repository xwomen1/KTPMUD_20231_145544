from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Path, status
from app.database import get_db
from app import models
from app.service.crud import userservice, employeeservice, clientservice, eventservice


def get_user_or_404(
    db_session: Session = Depends(get_db),
    user_id: int = Path(..., alias="id", ge=1),
) -> models.User:
    """
    Route dependency that retrieves a user by id or raises 404.
    """
    user = userservice.get(db_session=db_session, id_=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified user was not found.",
        )
    return user

def get_employee_or_404(
    db_session: Session = Depends(get_db),
    manv: str = Path(..., alias="manv", regex="^NV[0-9]{4}$"),
):
    """
    Route dependency that retrieves a user by id or raises 404.
    """
    employee = employeeservice.get(db_session=db_session, manv=manv)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified user was not found.",
        )
    return employee

def get_client_or_404(
    db_session: Session = Depends(get_db),
    makh: str = Path(..., alias="makh", regex="^KH[0-9]{4}$"),
):
    """
    Route dependency that retrieves a user by id or raises 404.
    """
    client = clientservice.get(db_session=db_session, makh=makh)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified user was not found.",
        )
    return client

def get_event_or_404(
    db_session: Session = Depends(get_db),
    mact: str = Path(..., alias="mact"),
):
    """
    Route dependency that retrieves a user by id or raises 404.
    """
    event = eventservice.get(db_session=db_session, mact=mact)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified event was not found.",
        )
    return event