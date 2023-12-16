from sqlalchemy.orm import Session

from app import models
from app.schemas.client import ClientBase, ClientOut, ClientUpdate

def get(db_session: Session, makh: str):
    return db_session.query(models.Client).filter(models.Client.makh == makh).first()


def get_multiple(
    db_session: Session, *, offset: int = 0, limit: int = 100
):
    return db_session.query(models.Client).offset(offset).limit(limit).all()


def create(db_session: Session, client_in: ClientBase, owner_id_get: int):
    db_obj = models.Client(**client_in.model_dump(), owner_id=owner_id_get)
    db_session.add(db_obj)
    db_session.commit()
    db_session.refresh(db_obj)
    return db_obj


def update(db_session: Session, client_update: ClientUpdate, makh: str):
    client_query = db_session.query(models.Client).filter(models.Client.makh == makh)

    client_query.update(client_update.model_dump(), synchronize_session=False)
    db_session.commit()

    return client_query.first()


def delete(db_session: Session, makh: str):
    client = get(db_session=db_session, makh=makh)
    db_session.query(models.User).filter(models.User.id == client.owner_id).delete()
    db_session.commit()
    return "Delete client makh = {makh} success".format(makh=makh)