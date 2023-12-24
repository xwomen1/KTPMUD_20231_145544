from typing import List, Optional
from fastapi import HTTPException, status, Path
from sqlalchemy.orm import Session

from app import models
from app.schemas.detail_event import DetailEventCreate, DetailEventUpdate


def get(db_session: Session, owner_event: str, id: int = Path(..., gt=0)):
    return db_session.query(models.DetailEvent).filter(models.DetailEvent.id==id).first()


def get_by_mact(db_session: Session, owner_event: str):
    return db_session.query(models.DetailEvent).filter(models.DetailEvent.owner_event == owner_event).all()

# def get_multiple(db_session: Session, offset: int = 0, limit: int = 100, search: str = ""):
#     return db_session.query(models.Event.name.contains(search)).offset(offset).limit(limit).all()



def create(db_session: Session, detail_event: DetailEventCreate):
    db_obj = models.DetailEvent(**detail_event.model_dump())
    db_session.add(db_obj)
    db_session.commit()
    db_session.refresh(db_obj)
    return db_obj


def update(db_session: Session, detail_event_update: DetailEventUpdate, id: int):
    detail_event_query = db_session.query(models.DetailEvent).filter(models.DetailEvent.id == id)

    detail_event_query.update(detail_event_update.model_dump(), synchronize_session=False)
    db_session.commit()

    return detail_event_query.first()

def delete(db_session: Session, mact: str):
    db_session.query(models.Event).filter(models.Event.mact == mact).delete()
    db_session.commit()
    return "Delete event have mact = {mact} success".format(mact=mact)