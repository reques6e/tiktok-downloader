from aiogram.dispatcher.filters.state import StatesGroup, State


class Newsletter(StatesGroup):
    send_post = State()
    waiting_for_button_text = State()
    waiting_for_button_url = State()