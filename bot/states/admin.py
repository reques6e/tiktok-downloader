from aiogram.dispatcher.filters.state import StatesGroup, State


class Newsletter(StatesGroup):
    send_post = State()