from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DATE, Float
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True)
    full_name = Column(String(), nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    gender = Column(Boolean, nullable=False)
    dateofbirth = Column(DATE, nullable=False)
    address = Column(String(255))
    phonenumber = Column(String(20), nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    is_active = Column(Boolean, nullable=False)


class Client(Base):
    __tablename__ = "client"

    makh = Column(Integer, unique=True, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", _constraint="owner_id_fk", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)


class Employee(Base):
    __tablename__ = "employee"

    manv = Column(Integer, unique=True, primary_key=True, nullable=False)
    salary = Column(Float, unique=True, nullable=False)
    ngaybatdaucongtac = Column(DATE, nullable=False)
    ngayketthuccongtac = Column(DATE, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", _constraint="employee_fk", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)


class Event(Base):
    __tablename__ = "event"

    mact = Column(String(20), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    detail = Column(String(100))
    owner = Column(Integer, ForeignKey("client.makh", _constraint="event_fk", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)


class DetailEvent(Base):
    __tablename__ = "detail_event"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    songuoithamgia = Column(Integer, nullable=False)
    created_at = Column(DATE, nullable=False, server_default=text('now()'))
    start_date = Column(DATE, nullable=False)
    end_date = Column(DATE, nullable=False)
    detail = Column(String)
    location = Column(String(100), nullable=False)
    mucphat = Column(Integer)

    owner_sk = Column(String(20), ForeignKey("event.mact", _constraint="owner_sk_fk", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

class HopDong(Base):
    __tablename__ = "contract"

    mahopdong = Column(String(50), primary_key=True, nullable=False, unique=True)
    giaidoan = Column(Integer, nullable=False)
    phithanhtoan = Column(Integer,nullable=False)
    motaphi = Column(String(100))
    phuongthuctt = Column(String(50), nullable=False)
    ngaytttheohd = Column(DATE, nullable=False)
    ngayttthucte = Column(DATE, nullable=False)

    owner_sk = Column(Integer, ForeignKey("detail_event.id", _constraint="hopdong_fk", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

class PhiPhat(Base):
    __tablename__ = "phiphat"

    id = Column(Integer, primary_key=True, nullable=False)
    phiphat = Column(Integer)
    mahopdong = Column(String(50), ForeignKey("contract.mahopdong", _constraint="phiphat_fk", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)