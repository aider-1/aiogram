from aiogram.fsm.state import State, StatesGroup

class Create(StatesGroup):
    name = State()
    contact_information = State()
    

class CreateDate(StatesGroup):
    date = State()
    theme = State()
    text_for_send = State()

class UpdateText(StatesGroup):
    new_text = State()

class CreateProfile(StatesGroup):
    name = State()
    email = State()
    email_password = State()

class Testing(StatesGroup):
    test_mail_to = State()
