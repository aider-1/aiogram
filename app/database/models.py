from typing import List, Optional
from sqlalchemy import CheckConstraint, Integer, String, ForeignKey, DateTime, URL
from sqlalchemy import Date as SQLAlchemyDate
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from enum import Enum
import os
from datetime import date as dt
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

db_url = URL.create(
    drivername="postgresql+asyncpg",
    username=os.getenv("DB_USERNAME", "postgres"),
    password=os.getenv("DB_PASSWORD", "root"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "sender"),
)

engine = create_async_engine(url=db_url, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase): pass

class Date(Base):
    __tablename__ = 'dates'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[dt] = mapped_column(SQLAlchemyDate(), unique=True)
    theme: Mapped[Optional[str]] = mapped_column(String(700), nullable=True)
    text_for_send: Mapped[Optional[str]] = mapped_column(
        String(700),
        nullable=True,
    )
    contractors: Mapped[List["Contractor"]] = relationship(back_populates='dates', secondary='contractor_date_link', lazy='selectin')

class ReceiptMethod(Enum):
    WHAPSAPP = "WHATSAPP"
    EMAIL = "EMAIL"

class Contractor(Base):
    __tablename__ = 'contractors'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    contact_information: Mapped[str] = mapped_column(String(50))
    method: Mapped[ReceiptMethod] = mapped_column(default=ReceiptMethod.EMAIL)
    dates: Mapped[List["Date"]] = relationship(back_populates='contractors', secondary='contractor_date_link', lazy='selectin')

class ContractorDateLink(Base):
    __tablename__ = 'contractor_date_link'
    
    contractor_id: Mapped[int] = mapped_column(ForeignKey('contractors.id'), primary_key=True)
    date_id: Mapped[int] = mapped_column(ForeignKey('dates.id'), primary_key=True)
    last_sent: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class Profile(Base):
    __tablename__ = "profile"
    __table_args__ = (CheckConstraint("id = 1", name="ck_profile_singleton"),)

    id: Mapped[int] = mapped_column(primary_key=True, server_default="1")
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    email_password: Mapped[str] = mapped_column(nullable=False)
