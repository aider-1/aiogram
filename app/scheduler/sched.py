from app.database.requests import get_contractors_for_sending, get_date_with_noload_by_today, get_profile
from app.scheduler.send_mail import send_email

async def send_scheduled_message():
    profile = await get_profile()
    if profile:
        contractors = await get_contractors_for_sending()
        date = await get_date_with_noload_by_today()
    
        for cont in contractors:
            print(cont.name)
    
        await send_email(mail_to=contractors, subject=date.theme, text=date.text_for_send, date=date.date,
        date_id=date.id, email=profile.email, email_password=profile.email_password, sender_name=profile.name) if contractors else print("Нет сообщений")
    else:
        print("Профиль не заполнен")
    