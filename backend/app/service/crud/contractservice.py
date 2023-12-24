from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.schemas.contract import ContractCreate, ContractUpdate


def get(db_session: Session, mahopdong: str):
    return db_session.query(models.HopDong).filter(models.HopDong.mahopdong == mahopdong).first()


def get_multiple(db_session: Session, offset: int = 0, limit: int = 100, search: str = ""):
    return db_session.query(models.HopDong.mahopdong.contains(search)).offset(offset).limit(limit).all()


def create(db_session: Session, contract: ContractCreate):
    db_obj = models.HopDong(**contract.model_dump())
    db_session.add(db_obj)
    db_session.commit()
    db_session.refresh(db_obj)
    return db_obj


def update(db_session: Session, contract_update: ContractUpdate, mahopdong: str):
    contract_query = db_session.query(models.HopDong).filter(models.HopDong.mahopdong == mahopdong)

    contract_query.update(contract_update.model_dump(), synchronize_session=False)
    db_session.commit()

    return contract_query.first()

def delete(db_session: Session, mahopdong: str):
    db_session.query(models.HopDong).filter(models.HopDong.mahopdong == mahopdong).delete()
    db_session.commit()
    return "Delete contract have mahopdong = {mahopdong} success".format(mahopdong=mahopdong)