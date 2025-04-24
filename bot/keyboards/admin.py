from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class AdminKeyboard:
    def __init__(self):
        pass

    def _main() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(
                text='Создать рассылку',
                callback_data='admin_newsletter'
            )
        )
        markup.add(
            InlineKeyboardButton(
                text='Добавить админа',
                callback_data='soon'
            ),
            InlineKeyboardButton(
                text='Снять админа',
                callback_data='soon'
            ),
        )

        return markup