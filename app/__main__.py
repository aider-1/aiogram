from aiogram import Bot, Dispatcher
from app.handlers.main_handler import router
from app.handlers.contracrors.create_contractor import contractors
from app.handlers.dates.create_date import dates
from app.handlers.dates.cal_navigate import cal
from app.handlers.contracrors.contractors_navigate import cont_route
from app.handlers.profile.profile import profile_router
from app.handlers.faq.faq_handler import faq_router
from app.handlers.logs.logs_handler import logs_router
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.scheduler.sched import send_scheduled_message
from apscheduler.triggers.cron import CronTrigger
from app.utils.config import tz_name as time_zone
from dotenv import load_dotenv
import asyncio
import logging

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

bot = Bot(token=bot_token)
dp = Dispatcher()

async def main():
    try:
        scheduler = AsyncIOScheduler()
        
        scheduler.add_job(
            send_scheduled_message,
            trigger=CronTrigger(minute="*/15", hour="7-21", timezone=time_zone), #"*/1"
            id="send_scheduled_message",
            coalesce=True,
            max_instances=1,
            misfire_grace_time=300
        )
        scheduler.start()
    
        dp.include_router(router=router)
        dp.include_router(router=contractors)
        dp.include_router(router=dates)
        dp.include_router(router=cal)
        dp.include_router(router=cont_route)
        dp.include_router(router=profile_router)
        dp.include_router(router=faq_router)
        dp.include_router(router=logs_router)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.exception("An error occurred: %s", e)
    finally:
        print("Shutting down...")
        scheduler.shutdown(wait=False)
        await bot.session.close()
        # await engine.dispose()
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
    