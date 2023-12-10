from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Employee
from app.schemas.employee import EmployeeBase, EmployeeOut
from app.service.passwordservice import get_password_hash, verify_password

def get(db_session: Session, makh: str) -> Optional[EmployeeOut]:
    return db_session.query(Employee).filter(Employee.makh == makh).first()


def get_multiple(
    db_session: Session, *, offset: int = 0, limit: int = 100
) -> List[Employee]:
    return db_session.query(Employee).offset(offset).limit(limit).all()


def create(db_session: Session, employee_in: EmployeeBase, owner_id_get: int):
    db_obj = Employee(**employee_in.model_dump(), owner_id=owner_id_get)
    db_session.add(db_obj)
    db_session.commit()
    db_session.refresh(db_obj)
    return db_obj


# def update(db_session: Session, user_in: User, user_change: UserUpdate):
#
#     if user_in is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
#
#     user_model = db_session.query(User).filter(User.id == user_in.get('id')).first()
#     if not verify_password(user_change.password, user_model.password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error on changed password')
#
#     user_model.password = get_password_hash(user_change.new_password)
#
#     db_session.add(user_model)
#     db_session.commit()
#     db_session.refresh(user_model)
#
#     return "Update password success"
#
# def delete(db_session: Session, id_: int):
#     db_session.query(User).filter(User.id == id_).delete()
#     db_session.commit()
#     return "Delete user id = {id} success".format(id=id_)