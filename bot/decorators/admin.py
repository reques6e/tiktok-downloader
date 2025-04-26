from functools import wraps
from aiogram import types

from bot.utils.database import Database
from config import OWNER_TELEGRAM_ID

db = Database()

def check_admin():
    """Проверка пользователя на админ права"""
    def decorator(func):
        @wraps(func)
        async def wrapper(message: types.Message | types.CallbackQuery, *args, **kwargs):
            if isinstance(message, types.Message): telegram_id = message.chat.id
            elif isinstance(message, types.CallbackQuery): telegram_id = message.message.chat.id

            print(f'OWNER: {OWNER_TELEGRAM_ID} AND {telegram_id}')
            if db.is_admin(telegram_id=telegram_id) or OWNER_TELEGRAM_ID == telegram_id:
                return await func(message, *args, **kwargs)
            else:
                text = 'У вас нет доступа к этому разделу!'
                if isinstance(message, types.Message): await message.answer(text=text)
                elif isinstance(message, types.CallbackQuery): await message.message.answer(text=text)
        return wrapper
    return decorator