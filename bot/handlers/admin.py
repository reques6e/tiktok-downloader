from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.exceptions import ChatNotFound
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.bot import dp, bot
from bot.keyboards.admin import AdminKeyboard
from bot.states.admin import Newsletter


@dp.message_handler(commands=['admin'], state='*')
async def admin(
    message: types.Message, state: FSMContext | None = None
):
    if state:
        await state.finish()

    msg = (
        '<b>🚀 Добро пожаловать в админ панель</b>'
    )
    
    msg += ( # делать нехуй было
        '\n\n'
        '<i>Мне очень жаль, моя любовь</i>\n'
        '<i>Я точно знаю, не забуду тебя</i>\n'
        '<i>Мне очень жаль и на восход</i>\n'
        '<i>Я улечу Москва-Владивосток</i>'
    )

    await message.answer(
        text=msg,
        reply_markup=AdminKeyboard._main()
    )

@dp.callback_query_handler(lambda c: c.data == 'admin_newsletter')
async def admin_newsletter(callback_query: types.CallbackQuery, state: FSMContext):
    message = await callback_query.message.edit_text(
        text='Отправьте пост'
    )
    await Newsletter.send_post.set()
    await state.set_data({
        'messageId': message.message_id
    })

@dp.message_handler(state=Newsletter.send_post, content_types=types.ContentType.ANY)
async def newsletter_send_post(message: types.Message, state: FSMContext):
    await message.delete()

    state_data = await state.get_data()
    # await state.finish()

    if message.media_group_id:
        return await bot.edit_message_text(
            text='Нельзя отправлять медиа-группу',
            chat_id=message.chat.id,
            message_id=state_data['messageId']
        )

    text = message.caption if message.caption else message.text

    if validate_html_structure(text) == False:
        return await message.answer(text='Ошибка в HTML')

    media_name = None
    if message.video:
        media_name = 'video'
        file_id = message.video.file_id
    elif message.photo:
        media_name = 'photo'
        file_id = message.photo[-1].file_id
    elif message.text:
        file_id = None
