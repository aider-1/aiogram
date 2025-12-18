from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.database.requests import get_logs_count, get_logs_page
from app.utils.generate import generate_text_logs

async def logs_buttons(page: int = 0):
    PER_PAGE = 5
    total = await get_logs_count()
    pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
    page = max(0, min(page, pages - 1))
    items = await get_logs_page(limit=PER_PAGE, offset=page * PER_PAGE)
    
    b = InlineKeyboardBuilder()
    
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"logs_page:{page-1}"))
        nav.append(InlineKeyboardButton(text=f"{page+1}/{pages}", callback_data="noop"))
    if page < pages-1:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"logs_page:{page+1}"))
    if nav:
        b.row(*nav, width=len(nav)) 

    b.row(
        InlineKeyboardButton(
            text="◀️ Назад", callback_data=f'back_start'
        )
    )
    
    text = ''
    if items:
        text = generate_text_logs(items)
    else:
        text = "Нет отправленных сообщений"
    
    return (b.as_markup(), text)
    