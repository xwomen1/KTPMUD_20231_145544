from fastapi import  Depends, HTTPException, status
from typing import Annotated

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from app.models import User
from app.config import settings

from jose import jwt, JWTError
from datetime import timedelta, datetime


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='api/v1/auth/login')


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_access_token(username: str, user_id: int,role: str, expires_delte: timedelta):
    encode = {
        'sub': username,
        'id': user_id,
        'role': role
    }

    expires = datetime.utcnow() + expires_delte
    encode.update({'exp' : expires})

    return jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail = 'Could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')