from bot.utils.database import Database
from bot.bot import dp, bot
from aiogram.types import (
    InputMediaVideo, InputMediaPhoto, InputMediaAnimation,
    InlineKeyboardButton, InlineKeyboardMarkup
)

database = Database()

medias = {
    'video': InputMediaVideo,
    'photo': InputMediaPhoto
}

async def newsletter(
    text: str, 
    file_id: str | None = None, 
    media_type: str | None = None, 
    markup: dict | None = None
) -> dict:
    # {"inline_keyboard": [[{"text": "ПОДПИСАТЬСЯ", "url": "https://t.me"}]]}

    SEND_ERROR = 0
    SEND_TRUE = 0

    users = database.get_users()
    for user in users:
        if media_type:
            try:
                if media_type == 'photo':
                    await bot.send_photo(
                        chat_id=user.telegram_id,
                        photo=file_id,
                        caption=text,
                        reply_markup=markup
                    )
                elif media_type == 'video':
                    await bot.send_video(
                        chat_id=user.telegram_id,
                        video=file_id,
                        caption=text,
                        reply_markup=markup
                    )
                SEND_TRUE += 1 
            except Exception as e:
                print(e)
                SEND_ERROR += 1
        else:
            try:
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=text,
                    reply_markup=markup
                )
                SEND_TRUE += 1
            except:
                SEND_ERROR += 1
    return {
        'true': SEND_TRUE,
        'false': SEND_ERROR
    }