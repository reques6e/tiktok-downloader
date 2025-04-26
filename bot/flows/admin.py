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
            media = medias[media_type](
                media=file_id,
                caption=text
            )
            try:
                await bot.send_media_group(
                    chat_id=user.telegram_id,
                    media=media,
                    reply_markup=markup
                )
                SEND_TRUE += 1 
            except:
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