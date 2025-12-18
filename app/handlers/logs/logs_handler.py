from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.logs_inline import logs_buttons

logs_router = Router()

@logs_router.callback_query(F.data == "logs")
async def main_logs(callback: CallbackQuery):
    await callback.answer()
    kb, text = await logs_buttons(page=0)
    
    await callback.message.edit_text(text=text, reply_markup=kb)
    
@logs_router.callback_query(F.data.startswith("logs_page:"))
async def logs_page(callback: CallbackQuery):
    await callback.answer()
    page = int(callback.data.replace("logs_page:", ""))
    kb, text = await logs_buttons(page=page)
    
    await callback.message.edit_text(text=text, reply_markup=kb)
