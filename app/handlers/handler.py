from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, callback_query
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from ..database.requests import get_date_by_id, get_contractor_by_id, delete_contractor, add_contractor_by_date_id, remove_contractor_from_date, delete_date
from ..keyboards.inline import show_dates as sh
from ..keyboards.inline import date_buttons as dt_bt
from ..keyboards.inline import contractor_buttons, contractor_list_buttons, add_contractor_by_date_buttons
from ..keyboards.inline import start_menu
from ..states.states import Create

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    # users = await User.get_users() получение контрагентов из бд для заполнения клавиатуры
    await message.answer("Выбери действие", reply_markup=start_menu()) #await show_users(users)  
    print(message.chat.id)
   
#Command("start")
@router.callback_query(F.data == "back_start")
async def back_to_start(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выбери действие", reply_markup=start_menu())
   
@router.callback_query(F.data == "list_dates")
async def show_dates(callback: CallbackQuery):
    kb = await sh()
    await callback.message.edit_text("выберите дату", reply_markup=kb)

@router.callback_query(F.data == 'list_contractors')
async def list_contractors(callback: CallbackQuery):
    await callback.answer()
    kb = await contractor_list_buttons()
    await callback.message.edit_text("Список контрагентов:", reply_markup=kb)

@router.callback_query(F.data.startswith('dt_'))
async def choose_date(callback: CallbackQuery):
    await callback.answer()
    date_id = callback.data.replace('dt_', '')
    chosen_date = await get_date_by_id(int(date_id))
    kb = dt_bt(chosen_date)
    
    await callback.message.edit_text(f'Дата отправки: {chosen_date.date}\nТема сообщения: {chosen_date.theme}\nТекст для отправки: {chosen_date.text_for_send}\nНажмите на контрагента, чтобы отвязать его от выбранной даты', reply_markup=kb)

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

@router.callback_query(F.data.startswith('cont_'))
async def contractor_info(callback: CallbackQuery):
    await callback.answer()
    cont_id = int(callback.data.replace('cont_', ''))
    
    contractor = await get_contractor_by_id(contractor_id=cont_id)
    await callback.message.edit_text(f"Имя контрагента: {contractor.name}\nКонтактные данные: {contractor.contact_information}", reply_markup=contractor_buttons(contractor_id=cont_id))

@router.callback_query(F.data.startswith('del_'))
async def del_contractor(callback: CallbackQuery):
    cont_id = callback.data.replace('del_', '')
    res = await delete_contractor(int(cont_id))
    await callback.answer()
    await list_contractors(callback)
    
    
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
    date_id = int(callback.data.replace("deldate_", ""))
    await delete_date(date_id)
    await show_dates(callback)

# async def back_date(message: Message, **kwargs):
#     date_id = kwargs["date_id"]
#     kb = us(date_id)
#     await message.edit_text(f'Дата отправки: {chosen_date.date}\nТема сообщения: {chosen_date.theme}\nТекст для отправки: {chosen_date.text_for_send}', reply_markup=kb)

# @router.callback_query(F.data.startswith('cont_'))
# async def all_contractors(callback: CallbackQuery):
#     await callback.answer()
#     id = callback.data.replace('cont_', '')
    
#     my_user = await User.get_one(id=id)
    
#     contractor_name = my_user.contractor_name
#     email = my_user.email
    
#     await callback.message.edit_text(f"Имя контрагента: {contractor_name}\nПочта: {email}\n")
    