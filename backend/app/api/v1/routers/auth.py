from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated
from sqlalchemy.orm import Session
from datetime import timedelta

from app.config import settings
from app.database import get_db
from app.schemas import token
from ..dependencies.auth import create_access_token, authenticate_user

router = APIRouter()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/login", response_model=token.Token)
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
