from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session

from ..utils import get_password_hash, verify_password
from .base import CRUDBase
from ..models import NguoiDung
from ..schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[NguoiDung, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[NguoiDung]:
            return db.query(NguoiDung).filter(NguoiDung.email == email).first()

    def create(self, db: Session, *, object: UserCreate) -> NguoiDung:
        db_obj = NguoiDung(email=object.email, hash_password=get_password_hash(object.password), role=UserCreate.role)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: NguoiDung, object: Union[UserUpdate, Dict[str, Any]]) -> NguoiDung:
        if isinstance(object, dict):
            update_data = object
        else:
            update_data = object.model_dump(exclude_unset=True)

        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"] #xoa doi tuong (tai vi khac kieu du lieu)
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=object)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[NguoiDung]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

Nguoidung = CRUDUser(NguoiDung)