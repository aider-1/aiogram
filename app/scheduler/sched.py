from app.database.requests import get_contractors_for_sending, get_date_with_noload_by_today, get_profile
from app.scheduler.send_mail import send_email
from app.utils.generate import EmailCrypto
from app.utils.config import secret_key

async def send_scheduled_message():
    profile = await get_profile()
    if profile:
        crypto = EmailCrypto(secret_key)
        crypto_password = crypto.decrypt_password(profile.email_password)
        # print(crypto_password)
        
        contractors = await get_contractors_for_sending()
        date = await get_date_with_noload_by_today()
    
        for cont in contractors:
            print(cont.name)
    
        await send_email(mail_to=contractors, subject=date.theme, text=date.text_for_send, date=date.date,
        date_id=date.id, email=profile.email, email_password=crypto_password, sender_name=profile.name, signature=profile.signature) if contractors else print("Нет сообщений")
    else:
        print("Профиль не заполнен")
    