from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.bot import dp, bot
from bot.keyboards.admin import AdminKeyboard
from bot.states.admin import Newsletter
from bot.utils.manage import validate_html_structure
from bot.flows.admin import newsletter


@dp.message_handler(commands=['admin'], state='*')
@dp.callback_query_handler(lambda c: c.data == 'admin_panel')
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
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='newsletter_out'
        )
    )

    message = await callback_query.message.edit_text(
        text='Отправьте пост',
        reply_markup=markup
    )

    await Newsletter.send_post.set()
    await state.set_data({
        'messageId': message.message_id
    })

@dp.message_handler(state=Newsletter.send_post, content_types=types.ContentType.ANY)
async def newsletter_send_post(message: types.Message, state: FSMContext):
    await message.delete()

    state_data = await state.get_data()

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

    reply_markup = InlineKeyboardMarkup()
    reply_markup.add(
        InlineKeyboardButton(
            text='Добавить кнопку',
            callback_data='newsletter_button_add'
        ),
        InlineKeyboardButton(
            text='Начать рассылку',
            callback_data='newsletter_start'
        )
    )
    reply_markup.add(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='newsletter_out'
        )
    )

    if media_name:
        media_method = {
            'photo': message.answer_photo,
            'video': message.answer_video
        }[media_name]
        
        msg_general = await media_method(
            **{media_name: file_id},
            caption=text,
            reply_markup=reply_markup
        )
    else:
        msg_general = await message.answer(
            text=text,
            reply_markup=reply_markup
        )


    await state.set_data({
        'text': text,
        'markup': {'inline_keyboard': []}, 
        'media': {
            'type': media_name, 
            'file_id': file_id
        },
        'messageId': msg_general.message_id 
    })

@dp.callback_query_handler(lambda c: c.data == 'newsletter_button_add', state=Newsletter.send_post)
async def newsletter_button_add(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    msg = await callback_query.message.answer(
        'Введите название для кнопки:',
        reply_markup=types.ForceReply(selective=True)
    )
    await Newsletter.waiting_for_button_text.set()
    await state.update_data(
        reply_message_id=msg.message_id
    )

@dp.message_handler(state=Newsletter.waiting_for_button_text, content_types=types.ContentType.TEXT)
async def process_button_text(message: types.Message, state: FSMContext):
    await message.delete()
    
    await state.update_data(button_text=message.text)

    state_data = await state.get_data()

    await bot.delete_message(chat_id=message.chat.id, message_id=state_data['reply_message_id'])

    msg = await message.answer(
        'Теперь введите URL для кнопки (начинается с http:// или https://):',
        reply_markup=types.ForceReply(selective=True)
    )
    await Newsletter.waiting_for_button_url.set()
    await state.update_data(reply_message_id=msg.message_id)

@dp.message_handler(state=Newsletter.waiting_for_button_url, content_types=types.ContentType.TEXT)
async def process_button_url(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    
    try:
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=state_data['reply_message_id']
        )
    except:
        pass
    await message.delete()
    
    if not message.text.startswith(('http://', 'https://')):
        return await message.answer("URL должен начинаться с http:// или https://")
    
    state_data = await state.get_data()
    text = state_data['text']
    media_type = state_data['media']['type']
    file_id = state_data['media']['file_id']
    
    markup = state_data.get('markup', {'inline_keyboard': []})
    markup['inline_keyboard'].append([{
        'text': state_data['button_text'],
        'url': message.text
    }])
    
    await state.update_data(markup=markup)
    
    reply_markup = InlineKeyboardMarkup(inline_keyboard=markup['inline_keyboard'])
    reply_markup.add(
        InlineKeyboardButton(
            text='Добавить ещё кнопку',
            callback_data='newsletter_button_add'
        ),
        InlineKeyboardButton(
            text='Начать рассылку',
            callback_data='newsletter_start'
        )
    )
    reply_markup.add(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='newsletter_out'
        )
    )
    
    if media_type:
        media_method = {
            'photo': bot.edit_message_caption,
            'video': bot.edit_message_caption
        }[media_type]
        
        await media_method(
            chat_id=message.chat.id,
            message_id=state_data['messageId'],
            caption=text,
            reply_markup=reply_markup
        )
    else:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=state_data['messageId'],
            text=text,
            reply_markup=reply_markup
        )
    
    await Newsletter.send_post.set()

@dp.callback_query_handler(lambda c: c.data == 'newsletter_start', state=Newsletter.send_post)
async def newsletter_start(callback_query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await state.finish()
    
    await callback_query.message.delete()
    message = await callback_query.message.answer(
        text='Начинаю рассылку...'
    )

    result = await newsletter(
        text=state_data['text'],
        file_id=state_data['media']['file_id'],
        media_type=state_data['media']['type'],
        markup=state_data['markup']
    )

    await bot.edit_message_text(
        text=(
            f'Успешно: {result["true"]}\n'
            f'Не удалось: {result["false"]}'
        ),
        chat_id=callback_query.message.chat.id,
        message_id=message.message_id
    )

@dp.callback_query_handler(lambda c: c.data == 'newsletter_out', state=Newsletter.send_post)
async def newsletter_out(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Рассылка отменана'
    )