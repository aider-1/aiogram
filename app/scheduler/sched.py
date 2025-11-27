from app.scheduler.send_mail import send_email
from app.database.requests import get_contractors_for_sending, set_last_sent_date

async def send_scheduled_message():
    date = await get_contractors_for_sending()

    if not date or not date.contractors:
        print("\n\n\n\n\n\n\n\nNo messages to send today.\n\n\n\n\n\n\n\n\n")
    elif date.contractors:
        subject = date.theme
        is_sent = False
        
        for cont in date.contractors:
            print(cont.contact_information)
        
        for contractor in date.contractors:
            mail_to = contractor.contact_information
            text = date.text_for_send
            
            result = await send_email(mail_to, subject, text)
            if 'OK' in result[1]:
                is_sent = True
        
        if is_sent:
            await set_last_sent_date(date.id)
    else:
        print("\n\n\n\nБля я хз\n\n\n\n\n")
            
        
