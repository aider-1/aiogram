from aiogram import Bot, Dispatcher
from app.handlers.main_handler import router
from app.handlers.contracrors.create_contractor import contractors
from app.handlers.dates.create_date import dates
from app.handlers.dates.cal_navigate import cal
from app.handlers.contracrors.contractors_navigate import cont_route
from app.handlers.profile.profile import profile_router
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.scheduler.sched import send_scheduled_message
from apscheduler.triggers.cron import CronTrigger
from app.database.models import engine
from dotenv import load_dotenv
import asyncio
import logging


load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
time_zone = os.getenv("TIME_ZONE", "Asia/Yekaterinburg")

bot = Bot(token=bot_token)
dp = Dispatcher()

async def main():
    try:
        scheduler = AsyncIOScheduler()
        
        scheduler.add_job(
            send_scheduled_message,
            trigger=CronTrigger(minute="*/15", hour="12-23", timezone=time_zone), #"*/1"
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
    