from aiogram import Router, F
from aiogram.types import Message, callback_query
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from ..database.models import Date
from ..database.requests import create_date
from ..states.states import CreateDate
from ..keyboards.inline import show_dates as sh

dates = Router()

@dates.callback_query(F.data == "create_date")
async def new_date(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CreateDate.date)
    await callback.message.answer('Введите дату')

@dates.message(CreateDate.date)
async def add_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text.strip())
    await state.set_state(CreateDate.theme)
    await message.answer("Введите тему сообщения")
    
@dates.message(CreateDate.theme)
async def add_theme(message: Message, state: FSMContext):
    await state.update_data(theme=message.text)
    await state.set_state(CreateDate.text_for_send)
    await message.answer("Введите текст для отправки")
    
@dates.message(CreateDate.text_for_send)
async def add_text(message: Message, state: FSMContext):
    await state.update_data(text_for_send=message.text)
    res = await state.get_data()
    await state.clear()
    from_create = await create_date(d=res["date"], th=res["theme"], text=res["text_for_send"])
    
    if from_create:
        await message.answer("Список обновлен!", reply_markup=await sh()) #добавить inline
    else:
        await message.answer("Такая дата уже существует", reply_markup=await sh())
    