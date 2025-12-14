from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, callback_query
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from ..database.requests import get_date_by_id, get_contractor_by_id, delete_contractor, add_contractor_by_date_id, remove_contractor_from_date, delete_date, get_profile
from ..keyboards.inline import show_dates as sh
from ..keyboards.inline import date_buttons as dt_bt
from ..keyboards.inline import contractor_buttons, contractor_list_buttons, add_contractor_by_date_buttons, show_years
from ..keyboards.inline import start_menu
from ..keyboards.profile_inline import create_profile
from ..states.states import UpdateText

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    is_profile = await get_profile()
    
    if is_profile:
        await message.answer("Выбери действие", reply_markup=start_menu())
    else:
        await message.answer("Заполните профиль для рассылки", reply_markup=create_profile())
    print(message.chat.id)
   
#Command("start")
@router.callback_query(F.data == "back_start")
async def back_to_start(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выбери действие", reply_markup=start_menu())
   
@router.callback_query(F.data == "calendar_years")
async def show_dates(callback: CallbackQuery):
    await callback.answer()
    kb = show_years()
    await callback.message.edit_text("Выберите год", reply_markup=kb)

@router.callback_query(F.data.startswith('from_'))
async def from_date(callback: CallbackQuery):
    await callback.answer()
    date_id = int(callback.data.replace('from_', ''))
    kb = await add_contractor_by_date_buttons(date_id)
    await callback.message.edit_text("Выберите контрагента для добавления на эту дату:", reply_markup=kb)
    
@router.callback_query(F.data.startswith('add_'))
async def add_contractor_to_date(callback: CallbackQuery):
    date_id, cont_id = map(int, callback.data.replace('add_', '').split('_'))
    result = await add_contractor_by_date_id(dt_id=date_id, cont_id=cont_id)
    if result:
        await callback.answer(text="Контрагент добавлен на дату", show_alert=True)
    else:
        await callback.answer(text="Ошибка при добавлении контрагента на дату", show_alert=True)
    
@router.callback_query(F.data.startswith('cl_'))
async def clean_contractor_from_date(callback: CallbackQuery):
    date_id, cont_id = map(int, callback.data.replace('cl_', '').split('_'))
    result = await remove_contractor_from_date(date_id=date_id, contractor_id=cont_id)
    if result:
        await callback.answer(text="Контрагент отвязан от даты", show_alert=True)
    else:
        await callback.answer(text="Ошибка при отвязке контрагента от даты", show_alert=True)

@router.callback_query(F.data.startswith('deldate_'))
async def del_date(callback: CallbackQuery):
    await callback.answer()
    date_id, year, month = map(str, callback.data.replace("deldate_", "").split("_"))
    await delete_date(int(date_id))
    await callback.message.edit_text(f"Год: {year}\nМесяц: {month}\nНажмите на дату, чтобы получить информацию о ней", reply_markup=await sh(month=month, year=year))
