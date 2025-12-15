from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.utils.generate import FAQ_KEYS

def faq_sections_kb():
    b = InlineKeyboardBuilder()
    for i, title in enumerate(FAQ_KEYS):
        b.row(InlineKeyboardButton(text=title, callback_data=f"faq_sec:{i}"))
    b.row(InlineKeyboardButton(text="◀️ Назад", callback_data="back_start"))
    return b.as_markup()

def faq_item_kb():
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="◀️ К разделам", callback_data="faq"))
    b.row(InlineKeyboardButton(text="◀️ В меню", callback_data="back_start"))
    return b.as_markup()