from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Добавить дату"), KeyboardButton(text="Список дат")]
], resize_keyboard=True, one_time_keyboard=True)
