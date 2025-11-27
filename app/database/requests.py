from .models import Contractor, Date
from .models import async_session
from sqlalchemy import select, or_, and_
from .models import ReceiptMethod
from datetime import datetime
from pytz import timezone
import logging
import os

tz_name = os.getenv("TIME_ZONE", "Asia/Yekaterinburg")

async def get_contractors() -> list[Contractor]:
    async with async_session() as session:
        query = select(Contractor)
        contractors = await session.execute(query)
        
        return contractors.scalars().all()

async def create_date(*, d, th, text) -> bool:
    async with async_session() as session:
        try:
            contractor = Date(date = d, theme = th, text_for_send = text)
            session.add(contractor)
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
        query = select(Date)
        date = await session.execute(query)
        
        return date.scalars().all()

async def get_date_by_id(id: int) -> Date:
    async with async_session() as session:
        date = await session.get_one(Date, id)
        return date
   
async def get_contractor_by_id(contractor_id: int) -> Contractor:
    async with async_session() as session:
        contractor = await session.get_one(Contractor, contractor_id)
        return contractor

async def delete_contractor(contractor_id: int) -> bool:
    async with async_session() as session:
        try:
            contractor = await session.get_one(Contractor, contractor_id)
            await session.delete(contractor)
            await session.commit()
            
            return True
        except Exception as e:
            print(e)
            return False

async def get_contractors_by_date_id(date_id: int) -> list[Contractor]:
    async with async_session() as session:
        date = await session.get_one(Date, date_id)
        return date.contractors

async def remove_contractor_from_date(*, date_id: int, contractor_id: int) -> bool:
    async with async_session() as session:
        try:
            date = await session.get_one(Date, date_id)
            contractor = await session.get_one(Contractor, contractor_id)
            
            date.contractors.remove(contractor)
            await session.commit()
            
            return True
        except Exception as e:
            print("remove cont: ", e)
            return False

async def get_contractors_for_sending() -> Date:
    async with async_session() as session:
        tz = timezone(tz_name)
        dt = datetime.now(tz).date()
        
        query = select(Date).where(
        and_(
            Date.date == str(dt.day),
            or_(Date.last_sent < dt, Date.last_sent == None),
            )
        )
        res = await session.scalar(query)
        return res if res else []

async def set_last_sent_date(date_id: int) -> None:
    async with async_session() as session:
        tz = timezone(tz_name)
        date = datetime.now(tz).date()
        
        bd_date = await session.get_one(Date, date_id)
        bd_date.last_sent = date
        await session.commit()

async def delete_date(date_id: int) -> bool:
    async with async_session() as session:
        try:
            date = await session.get_one(Date, date_id)
            await session.delete(date)
            await session.commit()
        
            return True
        except Exception as e:
            logging.error(e)
            return False
