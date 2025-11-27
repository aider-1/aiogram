from typing import List, Optional
from sqlalchemy import String, ForeignKey, DateTime, URL
from sqlalchemy import Date as SQLAlchemyDate
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from enum import Enum
import os
from datetime import date as dt
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL = os.getenv(
#     "DATABASE_URL",  # имя переменной окружения
#     "postgresql+asyncpg://postgres:root@host.docker.internal:5432/sender"  # дефолт, если переменная не задана
# )

db_url = URL.create(
    drivername="postgresql+asyncpg",
    username=os.getenv("DB_USERNAME", "postgres"),
    password=os.getenv("DB_PASSWORD", "root"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "sender"),
)

# db_url = "postgresql+asyncpg://postgres:root@localhost:5432/sender"

engine = create_async_engine(url=db_url, echo=True)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase): pass

class Date(Base):
    __tablename__ = 'dates'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(2), unique=True)
    theme: Mapped[str] = mapped_column(String(100))
    text_for_send: Mapped[str] = mapped_column(String(700))
    last_sent: Mapped[Optional[dt]] = mapped_column(SQLAlchemyDate(), nullable=True)
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
    
# async def async_main():
    # async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
