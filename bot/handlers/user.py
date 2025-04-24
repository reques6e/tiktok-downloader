import os

from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.exceptions import ChatNotFound
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hlink

from bot.bot import dp, bot
from bot.decorators.user import (
    allowed_links, check_db, timeout, in_channel
)
from bot.flows.user import download_video


@dp.message_handler(CommandStart(), state='*')
@check_db()
async def start(
    message: types.Message, state: FSMContext | None = None
):
    if state:
        await state.finish()
    
    await message.answer(
        text=(
            '<b>🚀 Добро пожаловать в <u>бота для скачивания видео</u> с <b>Instagram</b> и <b>TikTok</b>!</b>\n\n'
            '🎬 Просто отправьте ссылку на видео, и мы сделаем всё остальное!\n'
            '🔽 Начните прямо сейчас!'
        )
    )

@dp.message_handler(lambda message: message.text and message.text.startswith('https://'))
@in_channel()
@timeout()
@allowed_links()
async def handle_links(message: types.Message):
    process_message = await message.answer(
        text=(
            '📥 <b>Начинаю скачивание...</b>\n'
            'Пожалуйста, подождите ⏳'
        )
    )
    
    try:
        result = await download_video(url=message.text)

        with open(result, 'rb') as video:
            await message.answer_video(
                video=video
            )

        os.remove(result)
        
        await bot.edit_message_text(
            text=(
                '✅ <b>Ваше видео успешно подготовлено!</b>\n'
                '👇 Вы можете скачать его ниже.'
            ),
            chat_id=message.chat.id,
            message_id=process_message.message_id
        )
    except Exception as e:
        await message.answer(e)

@dp.message_handler(commands=['author'], state='*')
async def author(
    message: types.Message, state: FSMContext | None = None
):
    await message.answer(
        text=(
            '👨‍💻 <b>Автор:</b> <i>Астамур Ладария</i>\n\n'
            '🔗 <b>Мой GitHub:</b> <a href="https://github.com/reques6e">https://github.com/reques6e</a>\n\n'
            '📂 <b>Репозиторий проекта:</b> <a href="https://github.com/reques6e/tiktok-downloader">https://github.com/reques6e/tiktok-downloader</a>\n\n'
            '💡 Здесь вы найдёте код проекта, а также можете ознакомиться с моими другими работами и репозиториями.\n\n'
            '🎯 Если вам понравился бот — <b>поставьте звезду ⭐</b> в репозитории! 🌟\n\n'
            '🔄 Благодарю за использование и поддержку!'
        )
    )
