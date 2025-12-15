from aiosmtplib import SMTP, SMTPStatus
from email.headerregistry import Address
from email.message import EmailMessage
from app.database.models import Contractor
from app.database.requests import set_last_sent
from datetime import datetime
import logging

# email = os.getenv("EMAIL")
# email_password = os.getenv("EMAIL_PASSWORD")

async def send_email(*, mail_to: list[Contractor], subject: str, text: str, date: datetime.date, date_id: int, email: str, email_password: str, sender_name):
    try:    
        smtp_client = SMTP(hostname="smtp.mail.ru", port=2525, username=email, password=email_password) #2525  username=email
        async with smtp_client as sc:
            for cont in mail_to:
                print(f"\n\n\n\n{cont.name}\n\n\n")
                msg = EmailMessage()
                msg["From"] = f"{sender_name} <{email}>"
                msg["Subject"] = subject
                msg["To"] = cont.contact_information
                msg.set_content(text.format(имя=cont.name, дата=date.isoformat(), почта=cont.contact_information))
                msg.set_charset("utf-8")
                
                res = await sc.send_message(msg)
                
                if not res[0]:
                    await set_last_sent(date_id, cont.id)
                else:
                    logging.error(f"Send email ошибка вне except: {res}")
    except Exception as e:
        logging.error(f"Ошибка при отправке: {e}")
    
async def send_test_mail(*, test_email: str, test_email_password: str, name: str, mail_to: str):
    try:
        smtp_client = SMTP(hostname="smtp.mail.ru", port=2525, username=test_email, password=test_email_password) #2525  username=email
        async with smtp_client as sc:
            msg = EmailMessage()
            msg["From"] = f"{name} <{test_email}>"
            msg["Subject"] = "Тестирование"
            msg["To"] = mail_to
            msg.set_content("Тест почты")
            msg.set_charset("utf-8")
                
            res = await sc.send_message(msg)
            
            return res[1]
    except Exception as e:
        return e
    