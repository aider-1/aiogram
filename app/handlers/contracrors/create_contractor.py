from aiogram import Router
from aiogram import F
from aiogram.types import Message, callback_query
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from ...states.states import Create
from ...database.requests import add_contractor as add_contractor_to_db
from ...keyboards.inline import contractor_list_buttons

contractors = Router()

@contractors.callback_query(F.data == 'create_contractor')
async def add_contractor(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await state.set_state(Create.name)
    await callback.message.answer('Введите имя контрагента')
    
@contractors.message(Create.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Create.contact_information)
    await message.answer("Введите почту")
    
@contractors.message(Create.contact_information)
async def add_email(message: Message, state: FSMContext):
    await state.update_data(contact_information = message.text.strip())
    data = await state.get_data()
    await add_contractor_to_db(name=data['name'], contact_information=data['contact_information'])
    await message.answer("Список контрагентов обновлен", reply_markup=await contractor_list_buttons())
    
    await state.clear()
    