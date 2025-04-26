from functools import wraps
from aiogram import types

from bot.utils.database import Database


db = Database()

def check_admin():
    """Проверка пользователя на админ права"""
    def decorator(func):
        @wraps(func)
        async def wrapper(message: types.Message, *args, **kwargs):
            telegram_id = message.chat.id
            if db.is_admin(telegram_id=telegram_id):
                return await func(message, *args, **kwargs)
            else:
                await message.answer(text='У вас нет доступа к этому разделу!')
        return wrapper
    return decorator