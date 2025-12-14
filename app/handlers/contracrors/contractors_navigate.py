from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, callback_query
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.database.requests import get_date_by_id, get_contractor_by_id, delete_contractor, add_contractor_by_date_id, remove_contractor_from_date, delete_date
from app.keyboards.inline import show_dates as sh
from app.keyboards.inline import date_buttons as dt_bt
from app.keyboards.inline import contractor_buttons, contractor_list_buttons, add_contractor_by_date_buttons, show_years
from app.keyboards.inline import start_menu
from app.states.states import Create

cont_route = Router()

@cont_route.callback_query(F.data == 'list_contractors')
async def list_contractors(callback: CallbackQuery):
    await callback.answer()
    kb = await contractor_list_buttons()
    await callback.message.edit_text("Список контрагентов:", reply_markup=kb)

@cont_route.callback_query(F.data.startswith('cont_'))
async def contractor_info(callback: CallbackQuery):
    await callback.answer()
    cont_id = int(callback.data.replace('cont_', ''))
    
    contractor = await get_contractor_by_id(contractor_id=cont_id)
    await callback.message.edit_text(f"Имя контрагента: {contractor.name}\nКонтактные данные: {contractor.contact_information}", reply_markup=contractor_buttons(contractor_id=cont_id))

@cont_route.callback_query(F.data.startswith('del_'))
async def del_contractor(callback: CallbackQuery):
    cont_id = callback.data.replace('del_', '')
    res = await delete_contractor(int(cont_id))
    await callback.answer()
    await list_contractors(callback)