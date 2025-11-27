from aiosmtplib import SMTP, SMTPStatus
from email.message import EmailMessage
import os
from dotenv import load_dotenv
import ssl

load_dotenv()

email = os.getenv("EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")

async def send_email(mail_to: str, subject: str, text: str):
    try:
        msg = EmailMessage()
        msg["From"] = email
        msg["To"] = mail_to
        msg["Subject"] = subject
        msg.set_content(text)
        msg.set_charset("utf-8")
    
        smtp_client = SMTP(hostname="smtp.mail.ru", port=2525, username=email, password=email_password) #2525
        async with smtp_client as sc:
            res = await sc.send_message(msg)
            
            # smtp_client.vrfy
        # result = await aiosmtplib.send(
        #     msg,
        #     hostname="smtp.mail.ru",
        #     port=2525,
        #     start_tls=True,
        #     username=email,
        #     password=email_password,
        #     timeout=30
        # )
        
        return res
    
    except Exception as e:
        return f"Error sending email: {e}"
    