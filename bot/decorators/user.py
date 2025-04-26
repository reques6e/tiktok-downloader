from functools import wraps
from urllib.parse import urlparse
from aiogram import types

from bot.bot import bot
from bot.utils.database import Database
from config import TIME_OUT, CHANNEL_ID, CHANNEL_LINK


db = Database()

allowed_domains = [
    'tiktok.com',
    'www.tiktok.com',
    'instagram.com',
    'www.instagram.com',
]

def allowed_links():
    """Проверка ссылки"""
    def decorator(func):
        @wraps(func)
        async def wrapper(message: types.Message, *args, **kwargs):
            try:
                parsed_url = urlparse(message.text)
                if not parsed_url.scheme or not parsed_url.netloc:
                    return await message.answer(
                        text=(
                            '❌ <b>Некорректная ссылка!</b>\n'
                            'Пожалуйста, проверьте, что вы отправили правильный URL.\n\n'
                            'Пример:\n'
                            'https://www.instagram.com/reel/xxxxx/'
                        ),
                        parse_mode='HTML'
                    )
                domain = parsed_url.netloc.lower()
                if domain in allowed_domains:
                    return await func(message, *args, **kwargs)
                else:
                    await message.answer(
                        text=(
                            '⚠️ <b>Сервис не поддерживается</b>\n\n'
                            '✅ На данный момент поддерживаются только:\n'
                            '• Instagram 📸\n'
                            '• TikTok 🎵'
                        )
                    )
            except Exception:
                await message.answer(
                    text=(
                        '❌ <b>Ошибка обработки ссылки!</b>\n'
                        'Что-то пошло не так при обработке вашего запроса.\n'
                        'Пожалуйста, попробуйте ещё раз позже. Если ошибка повторится, сообщите нам.'
                    ),
                    parse_mode='HTML'
                )
        return wrapper
    return decorator

def check_db():
    """Проверка пользователя в бд"""
    def decorator(func):
        @wraps(func)
        async def wrapper(message: types.Message, *args, **kwargs):
            telegram_id = message.chat.id
            if db.user_exists(telegram_id=telegram_id) == False:
                db.create_user(telegram_id=telegram_id)
                db.add_timeout(telegram_id=telegram_id, duration_seconds=0)
            return await func(message, *args, **kwargs)
        return wrapper
    return decorator

def timeout():
    """Вадача и проверка тайм-аута"""
    def decorator(func):
        @wraps(func)
        async def wrapper(message: types.Message, *args, **kwargs):
            telegram_id = message.chat.id
            if db.check_timeout(telegram_id=telegram_id):
                return await message.answer(
                    text=(
                        f'⏳ <b>После каждого видео тайм-аут {TIME_OUT} секунд, пожалуйста подождите...</b>'
                    )
                )
            else:
                db.update_timeout(telegram_id=telegram_id, duration_seconds=TIME_OUT)
            return await func(message, *args, **kwargs)
        return wrapper
    return decorator

def in_channel():
    """Проверка, подписан пользователь в канал или нет"""
    def decorator(func):
        @wraps(func)
        async def wrapper(message: types.Message, *args, **kwargs):
            member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.chat.id)
            if member.status != 'left':
                return await func(message, *args, **kwargs)
            else:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(
                    text='Подписаться',
                    url=CHANNEL_LINK
                ))
                await message.answer(
                    text=(
                        '📢 <b>Перед скачиванием видео подпишитесь на наш канал!</b>\n\n'
                        '✅ Это обязательное условие для использования бота.'
                    ),
                    reply_markup=markup
                )
        return wrapper
    return decorator