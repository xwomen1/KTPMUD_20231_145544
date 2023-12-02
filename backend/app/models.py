from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DATE, Float
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class InfoUser(Base):
    __tablename__ = "infouser"

    code = Column(Integer, unique=True, primary_key=True, nullable=False)
    is_active = Column(Boolean, nullable=False)
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    gender = Column(Boolean, nullable=False)
    dateofbirth = Column(DATE, nullable=False)
    address = Column(String(255))
    phonenumber = Column(String(20), nullable=False, unique=True)
    salary = Column(Float)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

class Event(Base):
    __tablename__ = "sukien"

    maCT = Column(String(20), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    detail = Column(String(100))
    owner_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

class DetailEvent(Base):
    __tablename__ = "chitietsukien"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    user_code = Column(Integer, ForeignKey("infouser.code"), nullable=False)
    created_at = Column(DATE, nullable=False, server_default=text('now()'))
    ngaybatdau = Column(DATE, nullable=False)
    ngayketthuc = Column(DATE, nullable=False)
    detail = Column(String)
    diadiem = Column(String(100), nullable=False)
    mucphat = Column(Integer)

    owner_sk = Column(String(20), ForeignKey("sukien.maCT", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

class HopDong(Base):
    __tablename__ = "hopdong"

    mahopdong = Column(String(50), primary_key=True, nullable=False, unique=True)
    giaidoan = Column(Integer, nullable=False)
    phithanhtoan = Column(Integer,nullable=False)
    motaphi = Column(String(100))
    phuongthuctt = Column(String(50), nullable=False)
    ngaytttheohd = Column(DATE, nullable=False)
    ngayttthucte = Column(DATE, nullable=False)

    owner_sk = Column(Integer, ForeignKey("chitietsukien.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    owner = relationship("DetailEvent")

class PhiPhat(Base):
    __tablename__ = "phiphat"

    id = Column(Integer, primary_key=True, nullable=False)
    giaidoan = Column(Integer, nullable=False)
    phiphat = Column(Integer)
    mahopdong = Column(String(50), ForeignKey("hopdong.mahopdong", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)