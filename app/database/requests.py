import gc
from .models import Contractor, Date, ReceiptMethod, ContractorDateLink, Profile
from .models import async_session
from sqlalchemy import select, or_, and_, extract
from sqlalchemy.orm import noload
from datetime import datetime
from datetime import date as date_format
from pytz import timezone
import logging
import os
from dotenv import load_dotenv
from app.utils.generate import EmailCrypto
from app.utils.config import tz_name, secret_key


async def get_contractors() -> list[Contractor]:
    async with async_session() as session:
        query = select(Contractor)
        contractors = await session.execute(query)
        
        return contractors.scalars().all()

async def create_date(*, d, th, text) -> bool:
    async with async_session() as session:
        try:
            date = Date(date = date_format.fromisoformat(d), theme = th, text_for_send = text)
            session.add(date)
            await session.commit()

            return True
        except Exception as e:
            print(e)
            return False


async def add_contractor(*, name: str, contact_information: str):
    async with async_session() as session:
        try:
            contractor = Contractor(name=name, contact_information=contact_information)
    
            if '+7' in contact_information:
                contractor.method = ReceiptMethod.WHAPSAPP
        
            session.add(contractor)
            await session.commit()
        except Exception as e:
            print("add cont: ", e)

async def add_contractor_by_date_id(*, dt_id: int, cont_id: int) -> bool:
    async with async_session() as session:
        try:
            # session.expunge_all()
            
            date = await session.get_one(Date, dt_id)
            contractor = await session.get_one(Contractor, cont_id)
        
            date.contractors.extend([contractor])
            await session.commit()
            
            return True
        except Exception as e:
            print("add cont: ", e)
            return False

async def get_dates() -> Date:
    async with async_session() as session:
        # session.expunge_all()
        
        query = select(Date)
        date = await session.execute(query)
        
        return date.scalars().all()

async def get_date_by_id(id: int) -> Date:
    async with async_session() as session:
        # session.expunge_all()
        
        date = await session.get(Date, id)
        return date if date else None

async def get_date_with_noload(date_id: int) -> Date:
    async with async_session() as session:
        date = await session.get(Date, date_id, options=[noload(Date.contractors)])
        
        return date

async def get_date_with_noload_by_today() -> Date:
    async with async_session() as session:
        tz = timezone(tz_name)
        
        today = datetime.now(tz=tz).date().today()
        query = select(Date).where(Date.date == today).options(noload(Date.contractors))
        date = await session.execute(query)
        
        return date.scalar()

async def get_dates_by_year_month(*, year: int, month: int) -> list[Date]:
    async with async_session() as session:
        query = select(Date).where((extract("year", Date.date) == year), (extract("month", Date.date) == month)).options(noload(Date.contractors))
        date = await session.execute(query)
        res = date.scalars()
        
        return res if res else None

async def get_contractor_by_id(contractor_id: int) -> Contractor:
    async with async_session() as session:
        # session.expunge_all()
        
        contractor = await session.get_one(Contractor, contractor_id)
        return contractor

async def delete_contractor(contractor_id: int) -> bool:
    async with async_session() as session:
        try:
            # session.expunge_all()
            
            contractor = await session.get_one(Contractor, contractor_id)
            await session.delete(contractor)
            await session.commit()
            
            return True
        except Exception as e:
            print(e)
            return False

async def get_contractors_by_date_id(date_id: int) -> list[Contractor]:
    async with async_session() as session:
        # session.expunge_all()
        
        date = await session.get_one(Date, date_id)
        return date.contractors

async def remove_contractor_from_date(*, date_id: int, contractor_id: int) -> bool:
    async with async_session() as session:
        try:
            # session.expunge_all()
            
            date = await session.get_one(Date, date_id)
            contractor = await session.get_one(Contractor, contractor_id)
            
            date.contractors.remove(contractor)
            await session.commit()
            
            return True
        except Exception as e:
            print("remove cont: ", e)
            return False

async def delete_date(date_id: int) -> bool:
    async with async_session() as session:
        try:
            # session.expunge_all()
            
            date = await session.get_one(Date, date_id)
            await session.delete(date)
            await session.commit()
        
            return True
        except Exception as e:
            logging.error(e)
            return False

async def is_year(*, year: int) -> bool:
    async with async_session() as session:
        # session.expunge_all()
        
        query = select(Date).where(extract("year", Date.date) == year)
        res = await session.scalar(query)
        
        await session.close()
        return True if res else False
    
async def is_date(*, date: datetime.date) -> Date | None:
    async with async_session() as session:
        query = select(Date).where(Date.date == date)
        dt = await session.execute(query)
        res = dt.scalar_one_or_none()
        
        return res if res else None
    
async def get_contractors_for_sending():
    async with async_session() as session:
        tz = timezone(tz_name)
        dt = datetime.now(tz=tz).date().today()
        stmt = (
            select(Contractor)
            .join(ContractorDateLink, ContractorDateLink.contractor_id == Contractor.id)
            .join(Date, Date.id == ContractorDateLink.date_id)
            .where(Date.date == dt, ContractorDateLink.last_sent.is_(None))
            .options(noload(Contractor.dates))
        )
        res = await session.execute(stmt)
        return res.scalars().all()
    
async def set_last_sent(date_id: int, cont_id: int):
    async with async_session() as session:
        query = select(ContractorDateLink).where(ContractorDateLink.date_id == date_id, ContractorDateLink.contractor_id == cont_id)
        data = await session.execute(query)
        res = data.scalar()
        
        res.last_sent = datetime.now(tz=timezone(tz_name))
        
        await session.commit()
    
async def get_profile() -> Profile | None:
    async with async_session() as session:
        res = await session.scalar(select(Profile))

        return res if res else None
    
async def set_profile(*, name: str, email: str, email_password: str):
    async with async_session() as session:
        crypto = EmailCrypto(secret_key)
        crypto_password = crypto.encrypt_password(email_password)
        
        profile = Profile(name=name, email=email, email_password=crypto_password)
        session.add(profile)
        
        await session.commit()

async def update_profile(*, name: str, email: str, email_password: str):
    async with async_session() as session:
        crypto = EmailCrypto(secret_key)
        crypto_password = crypto.encrypt_password(email_password)
        
        current_profile = await session.scalar(select(Profile))
        current_profile.name = name
        current_profile.email = email
        current_profile.email_password = crypto_password
        
        await session.commit()
