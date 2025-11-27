from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..database.models import Date
from ..database.requests import get_contractors, get_dates
from ..database.models import Contractor, Date

def start_menu():
    buttons = [
        [InlineKeyboardButton(text="Контрагенты", callback_data="list_contractors")],
        [InlineKeyboardButton(text="Даты", callback_data="list_dates")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def contractor_list_buttons():
    contractors = await get_contractors()
    builder = InlineKeyboardBuilder()
    for cont in contractors:
        builder.add(  #row
            InlineKeyboardButton(
                text=cont.name,
                callback_data=f'cont_{cont.id}'
            )
        )
    
    builder.row(
        InlineKeyboardButton(
            text="Назад", callback_data="back_start"
        ),
        InlineKeyboardButton(
            text="Создать контрагента", callback_data="create_contractor"
        )
    )
    
    builder.adjust(2)
    return builder.as_markup()

def contractor_buttons(contractor_id: int):
    buttons = [
        [
            InlineKeyboardButton(text="Удалить", callback_data=f'del_{contractor_id}'),
            InlineKeyboardButton(text="Назад", callback_data=f'list_contractors')
        ]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def date_buttons(date: Date):
    builder = InlineKeyboardBuilder()
    contractors = date.contractors
    if contractors:
        for cont in contractors:
            builder.row(
                InlineKeyboardButton(
                    text=cont.name,
                    callback_data=f'cl_{date.id}_{cont.id}' #добавить функционал для date-contractor
                )
            )
    
    builder.row(
        InlineKeyboardButton(
            text='Добавить',
            callback_data=f'from_{date.id}'
        ),
        InlineKeyboardButton(
            text="Назад", callback_data="list_dates"
        ),
        InlineKeyboardButton(
            text="Удалить дату", callback_data=f"deldate_{date.id}"
        )
    )
    
    builder.adjust(2)
    return builder.as_markup()

async def show_dates():
    builder = InlineKeyboardBuilder()
    dates = await get_dates()
    
    for date in dates:
        builder.row(
            InlineKeyboardButton(
                text=date.date,
                callback_data=f"dt_{date.id}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(
            text="Назад", callback_data="back_start"
        ),
        InlineKeyboardButton(
            text="Добавить дату", callback_data="create_date"
        )
    )
    
    builder.adjust(2)
    return builder.as_markup()

async def add_contractor_by_date_buttons(date_id: int):
    builder = InlineKeyboardBuilder()
    contractors = await get_contractors()
    
    for cont in contractors:
        builder.row(
            InlineKeyboardButton(
                text=cont.name,
                callback_data=f'add_{date_id}_{cont.id}'
            )
        )
        
    builder.row(
        InlineKeyboardButton(
            text="Назад", callback_data=f'dt_{date_id}'
        )
    )
    
    builder.adjust(2)
    return builder.as_markup()

# def clean_contractor_by_date_buttons(date_id: int, contractor_id: int):
#     builder = InlineKeyboardBuilder()
#     builder.row(
#         InlineKeyboardButton(
#             text="Отвязать", callback_data=f'cl_{date_id}_{contractor_id}'
#         ),
#         InlineKeyboardButton(
#             text="Назад", callback_data=f'dt_{date_id}'
#         )
#     )
    
#     builder.adjust(2)
#     return builder.as_markup()
