from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DATE
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    fullname = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    gender = Column(Boolean, nullable=False)
    dateofbirth = Column(DATE, nullable=False)
    phonenumber = Column(String(20), nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    role = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)

class Employee(Base):
    __tablename__ = "employee"

    manv = Column(String, primary_key=True, nullable=False)
    ngaybatdaucongtac = Column(DATE, nullable=False)
    ngayketthuccongtac = Column(DATE, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", _constraint="employee_fk", ondelete="CASCADE"), nullable=False)

    users = relationship("User", backref="employees")


class Client(Base):
    __tablename__ = "client"

    makh = Column(Integer, primary_key=True, nullable=False)
    address = Column(String(255))
    owner_id = Column(Integer, ForeignKey("users.id", _constraint="client_fk", ondelete="CASCADE"), nullable=False)

    users = relationship("User", backref="client")


class Event(Base):
    __tablename__ = "event"

    mact = Column(String(20), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    detail = Column(String(100))
    ngaybatdau = Column(DATE, nullable=False)
    ngayketthuc = Column(DATE, nullable=False)
    owner = Column(Integer, ForeignKey("client.makh", _constraint="event_fk", ondelete="CASCADE"), nullable=False)


class DetailEvent(Base):
    __tablename__ = "detail_event"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    songuoithamgia = Column(Integer, nullable=False)
    ngaybatdau = Column(DATE, nullable=False)
    ngayketthuc = Column(DATE, nullable=False)
    detail = Column(String)
    location = Column(String(100), nullable=False)

    owner_event = Column(String(20), ForeignKey("event.mact", _constraint="owner_event_fk", ondelete="CASCADE"), nullable=False)

    event = relationship("Event", backref="detail_event")

class HopDong(Base):
    __tablename__ = "contract"

    mahopdong = Column(String(50), primary_key=True, nullable=False, unique=True)
    giaidoan = Column(Integer, nullable=False)
    phithanhtoan = Column(Integer,nullable=False)
    motaphi = Column(String(100))
    pt_thanhtoan = Column(String(50), nullable=False)
    ngaytttheohd = Column(DATE, nullable=False)
    ngayttthucte = Column(DATE, nullable=False)

    owner = Column(Integer, ForeignKey("event.mact", _constraint="hopdong_fk", ondelete="CASCADE"), nullable=False)

class PhiPhat(Base):
    __tablename__ = "phiphat"

    id = Column(Integer, primary_key=True, nullable=False)
    phiphat = Column(Integer)
    lydo = Column(String, nullable=False)
    owner_detail = Column(String(50), ForeignKey("detail_event.id", _constraint="phiphat_fk", ondelete="CASCADE"), nullable=False)