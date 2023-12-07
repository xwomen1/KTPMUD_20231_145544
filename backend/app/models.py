from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DATE, Float
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    full_name = Column(String(), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
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

    makh = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String(), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    gender = Column(Boolean, nullable=False)
    dateofbirth = Column(DATE, nullable=False)
    address = Column(String(255))
    phonenumber = Column(String(20), nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    is_active = Column(Boolean, nullable=False)

class Employee(Base):
    __tablename__ = "employee"

    manv = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String(), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    gender = Column(Boolean, nullable=False)
    dateofbirth = Column(DATE, nullable=False)
    address = Column(String(255))
    phonenumber = Column(String(20), nullable=False, unique=True)
    salary = Column(Float, unique=True, nullable=False)
    ngaybatdaucongtac = Column(DATE, nullable=False)
    ngayketthuccongtac = Column(DATE, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    is_active = Column(Boolean, nullable=False)


class Event(Base):
    __tablename__ = "event"

    mact = Column(String(20), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    detail = Column(String(100))
    owner = Column(Integer, ForeignKey("client.makh", _constraint="event_fk", ondelete="CASCADE"), nullable=False)


class DetailEvent(Base):
    __tablename__ = "detail_event"

    id = Column(Integer, primary_key=True, nullable=False)
    songuoithamgia = Column(Integer, nullable=False)
    start_date = Column(DATE, nullable=False)
    end_date = Column(DATE, nullable=False)
    detail = Column(String)
    location = Column(String(100), nullable=False)
    mucphat = Column(Integer)

    owner_event = Column(String(20), ForeignKey("event.mact", _constraint="owner_sk_fk", ondelete="CASCADE"), nullable=False)

class HopDong(Base):
    __tablename__ = "contract"

    mahopdong = Column(String(50), primary_key=True, nullable=False)
    phithanhtoan = Column(Integer,nullable=False)
    motaphi = Column(String(100))
    phuongthuctt = Column(String(50), nullable=False)
    ngaytttheohd = Column(DATE, nullable=False)
    ngayttthucte = Column(DATE, nullable=False)
    giaidoan = Column(Integer, nullable=False)

    owner_event = Column(Integer, ForeignKey("event.mact", _constraint="hopdong_fk", ondelete="CASCADE"), nullable=False, unique=True)

class PhiPhat(Base):
    __tablename__ = "phiphat"

    id = Column(Integer, primary_key=True, nullable=False)
    phiphat = Column(Integer)
    mahopdong = Column(String(50), ForeignKey("contract.mahopdong", _constraint="phiphat_fk", ondelete="CASCADE"), nullable=False)