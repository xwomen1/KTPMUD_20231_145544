from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
from .schemas import token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY
# Algorithm
# Expriation time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token_verify: str, credentials_exception):
    try:
        payload = jwt.decode(token_verify, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = token.Token(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token_verify: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token_verify = verify_access_token(token_verify, credentials_exception)

    user = db.query(models.NguoiDung).filter(models.NguoiDung.id==token_verify.id).first()

    return user