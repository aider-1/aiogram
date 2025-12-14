from aiogram import Router, F
from aiogram.types import Message, callback_query
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.states.states import CreateProfile, Testing
from app.database.requests import get_profile, set_profile, update_profile
from app.keyboards.profile_inline import show_profile, create_profile
from app.scheduler.send_mail import send_test_mail

profile_router = Router()

@profile_router.callback_query(F.data == "profile")
async def main_profile(callback: CallbackQuery):
    await callback.answer()
    profile = await get_profile()
    
    await callback.message.edit_text(f"Имя отправителя: {profile.name}\nПочта: {profile.email}", reply_markup=show_profile()) if profile else print("Ошибка при взаимодействии с профилем")
    
@profile_router.callback_query(F.data == "create_profile")
async def start_create_profile(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(CreateProfile.name)
    await callback.message.answer("Введите имя, которое будет указываться при отправке сообщения на почту")
    
@profile_router.message(CreateProfile.name)
async def set_name_profile(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateProfile.email)
    await message.answer("Введите свою почту")
    
@profile_router.message(CreateProfile.email)
async def set_email_profile(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(CreateProfile.email_password)
    await message.answer("Введите пароль электронной почты (создайте пароль только для отправки сообщений ради безопасности)")
    
@profile_router.message(CreateProfile.email_password)
async def set_email_password_profile(message: Message, state: FSMContext):
    await state.update_data(email_password=message.text)
    data = await state.get_data()
    
    is_profile = await get_profile()
    
    await set_profile(name=data.get("name"), email=data.get("email"), email_password=data.get("email_password")) if not is_profile else await update_profile(name=data.get("name"), email=data.get("email"), email_password=data.get("email_password"))
    await state.clear()
    
    profile = await get_profile()
    
    if profile:
        await message.answer(f"Имя отправителя: {profile.name}\nПочта: {profile.email}", reply_markup=show_profile())
    else:
        await message.answer("Произошла ошибка при заполнении профиля", reply_markup=create_profile())

@profile_router.callback_query(F.data == "send_test_mail")
async def email_testing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    # profile = await get_profile()
    await state.set_state(Testing.test_mail_to)
    await callback.message.answer("Введите почту, на которую хотите отправить тестовое сообщение")
    
@profile_router.message(Testing.test_mail_to)
async def getting_test_email(message: Message, state: FSMContext):
    await state.clear()
    profile = await get_profile()
    
    res = await send_test_mail(test_email=profile.email, test_email_password=profile.email_password, name=profile.name, mail_to=message.text)
    await message.answer(f"Имя отправителя: {profile.name}\nПочта: {profile.email}\nСтатус отправки: {res}", reply_markup=show_profile())
