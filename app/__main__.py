import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.handlers.handler import router
from app.handlers.create_contractor import contractors
from app.handlers.create_date import dates
# from app.database.models import async_main
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.database.models import engine
from app.scheduler.sched import send_scheduled_message
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
time_zone = os.getenv("TIME_ZONE", "Asia/Yekaterinburg")

bot = Bot(token=bot_token)
dp = Dispatcher()

async def main():
    try:
        scheduler = AsyncIOScheduler()
        # await async_main()
        
        scheduler.add_job(
            send_scheduled_message,
            trigger=CronTrigger(minute="*/30", hour="12-22", timezone=time_zone),
            id="send_scheduled_message",
            coalesce=True,
            max_instances=1,
            misfire_grace_time=300
        )
        
        scheduler.start()
    
        dp.include_router(router=router)
        dp.include_router(router=contractors)
        dp.include_router(router=dates)
    
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
    