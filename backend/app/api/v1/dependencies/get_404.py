from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Path, status
from app.database import get_db
from app import models
from app.service import userservice
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