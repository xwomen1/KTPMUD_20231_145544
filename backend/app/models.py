from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DATE, Float
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class NguoiDung(Base):
    __tablename__ = "nguoidung"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    describe = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
class NhanVien(Base):
    __tablename__ = "nhanvien"

    maNV = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(255), nullable=False)
    gender = Column(Boolean, nullable=False)
    dateofbirth = Column(DATE, nullable=False)
    diachi = Column(String(255))
    phonenumber = Column(String(20), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    cosalary = Column(Float, nullable=False)

    owner_id = Column(Integer, ForeignKey("nguoidung.id", ondelete= "CASCADE"), nullable= False)


class KhachHang(Base):
    __tablename__ = "khachhang"

    maKH = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(255), nullable=False)
    diachi = Column(String(255))
    phonenumber = Column(String(20), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)

    owner_id = Column(Integer, ForeignKey("nguoidung.id", ondelete= "CASCADE"), nullable= False)


class Event(Base):
    __tablename__ = "sukien"

    maCT = Column(String(20), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    detail = Column(String(100))
    owner_id = Column(Integer, ForeignKey("nguoidung.id"), nullable=False)

    owner = relationship("NguoiDung")

class DetailEvent(Base):
    __tablename__ = "chitietsukien"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    maKH = Column(Integer, ForeignKey("khachhang.maKH"), nullable=False)
    maCT = Column(String(20), ForeignKey("sukien.maCT"), nullable=False)
    maNV = Column(Integer, ForeignKey("nhanvien.maNV"), nullable=False)
    created_at = Column(DATE, nullable=False, server_default=text('now()'))
    ngaybatdau = Column(DATE, nullable=False)
    ngayketthuc = Column(DATE, nullable=False)
    detail = Column(String)
    songuoithamgia = Column(Integer, nullable=False)
    diadiem = Column(String(100), nullable=False)
    mucphat = Column(Integer)

class HopDong(Base):
    __tablename__ = "hopdong"

    mahopdong = Column(String(50), primary_key=True, nullable=False, unique=True)
    giaidoan = Column(Integer, nullable=False)
    phithanhtoan = Column(Integer,nullable=False)
    motaphi = Column(String(100))
    phuongthuctt = Column(String(50), nullable=False)
    ngaytttheohd = Column(DATE, nullable=False)
    ngayttthucte = Column(DATE, nullable=False)

    owner_sk = Column(Integer, ForeignKey("chitietsukien.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("DetailEvent")

class PhiPhat(Base):
    __tablename__ = "phiphat"

    id = Column(Integer, primary_key=True, nullable=False)
    giaidoan = Column(Integer, nullable=False)
    phiphat = Column(Integer)
    mahopdong = Column(String(50), ForeignKey("hopdong.mahopdong", ondelete="CASCADE"), nullable=False)