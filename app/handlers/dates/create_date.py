from aiogram import Router, F
from aiogram.types import Message, callback_query
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from ...database.models import Date
from ...database.requests import create_date
from ...states.states import CreateDate
from ...keyboards.inline import show_dates as sh

dates = Router()

@dates.callback_query(F.data.startswith("create_date_"))
async def new_date(callback: CallbackQuery, state: FSMContext):
    dt = callback.data.replace("create_date_", "")
    await state.update_data(date=dt)
    await state.set_state(CreateDate.theme)
    await callback.message.answer("Введите тему сообщения")
    
@dates.message(CreateDate.theme)
async def add_theme(message: Message, state: FSMContext):
    await state.update_data(theme=message.text)
    await state.set_state(CreateDate.text_for_send)
    await message.answer("Введите текст для отправки\nИспользуйте вставки типа {имя}, {почта}, {дата}, чтобы использовать информацио о получателе/дате")
    
@dates.message(CreateDate.text_for_send)
async def add_text(message: Message, state: FSMContext):
    await state.update_data(text_for_send=message.text)
    res = await state.get_data()
    from_create = await create_date(d=res.get("date"), th=res.get("theme"), text=res.get("text_for_send"))
    year = int(res.get("date").split("-")[0])
    month = int(res.get("date").split("-")[1])
    if from_create:
        await message.answer(f"Год: {year}\nМесяц: {month}\nНажмите на дату, чтобы получить информацию о ней\nСтатус: дата успешно создана", reply_markup=await sh(year=year, month=month)) #добавить inline
    else:
        await message.answer(f"Год: {year}\nМесяц: {month}\nНажмите на дату, чтобы получить информацию о ней\nСтатус: ошибка", reply_markup=await sh(year=year, month=month))
        
    await state.clear()
