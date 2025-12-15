from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_profile():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(
            text="Создать профиль",
            callback_data="create_profile"
        )
    )
    
    builder.adjust(2)
    return builder.as_markup()

def show_profile():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="✏️Изменить профиль", callback_data="create_profile")
    )
    
    builder.row(
        InlineKeyboardButton(text="✉️Отправить тестовое сообщение", callback_data="send_test_mail")
    )
    
    builder.row(
        InlineKeyboardButton(text="◀️Назад", callback_data="back_start")
    )
    
    builder.adjust(2)
    return builder.as_markup()