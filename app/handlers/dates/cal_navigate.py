import gc
from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, callback_query
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.database.requests import get_date_by_id
from app.keyboards.inline import show_dates, show_months, generate_date_buttons, date_buttons


cal = Router()

mnth = 1

@cal.callback_query(F.data.startswith("yr_"))
async def years_main(callback: CallbackQuery):
    await callback.answer()
    chose_year = int(callback.data.replace("yr_", ""))
    kb = show_months(year=chose_year)
    
    await callback.message.edit_text("Выберите месяц", reply_markup=kb)
    
@cal.callback_query(F.data.startswith("mth_"))
async def choose_months(callback: CallbackQuery):
    await callback.answer()
    year, month = map(str, callback.data.replace("mth_", "").split("_"))
    
    kb = await show_dates(month=month, year=year)
    await callback.message.edit_text(f"Год: {year}\nМесяц: {month}\nНажмите на дату, чтобы получить информацию о ней\nДаты выводятся в формате ПН-ВС", reply_markup=kb)
    
@cal.callback_query(F.data.startswith('dt_'))
async def choose_date(callback: CallbackQuery):
    await callback.answer()
    raw = callback.data.replace("dt_", "")
    
    kb = generate_date_buttons(raw_date=raw)
    await callback.message.edit_text("Пустая дата", reply_markup=kb)

@cal.callback_query(F.data.startswith('dtid_'))
async def exist_date(callback: CallbackQuery):
    await callback.answer()
    date_id = int(callback.data.replace("dtid_", ""))
    date_info = await get_date_by_id(id=date_id)
    
    kb = date_buttons(date_info)
    await callback.message.edit_text(f"📅Дата отправки: {date_info.date.isoformat()}\n🧾Тема сообщения: {date_info.theme}\n"
    f"✉️Текст для отправки: {date_info.text_for_send}\n📌Нажмите на контрагента, чтобы отвязать его от выбранной даты", reply_markup=kb)

# kb = date_buttons(date_info)
#         await callback.message.edit_text(f"Дата отправки: {date_info.date.isoformat()}\nТема сообщения: {date_info.theme}\n"
#         f"Текст для отправки: {date_info.text_for_send}\nНажмите на контрагента, чтобы отвязать его от выбранной даты", reply_markup=kb)