from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.faq_keyboard import faq_item_kb, faq_sections_kb
from app.utils.generate import FAQ, FAQ_KEYS

faq_router = Router()

@faq_router.callback_query(F.data == "faq")
async def faq_root(cb: CallbackQuery):
    await cb.answer()
    await cb.message.edit_text("FAQ — выберите раздел:", reply_markup=faq_sections_kb())

@faq_router.callback_query(F.data.startswith("faq_sec:"))
async def faq_section(cb: CallbackQuery):
    await cb.answer()
    i = int(cb.data.split(":", 1)[1])
    title = FAQ_KEYS[i]
    text = "\n".join(f"• {x}" for x in FAQ[title])
    await cb.message.edit_text(f"{title}\n\n{text}", reply_markup=faq_item_kb())