import asyncio

from aiogram import executor
from aiogram.types import BotCommand

from bot.bot import dp, bot
from bot.handlers import (
    admin, user
)


async def set_commands():
    commands = [
        BotCommand(command='start', description='Запустить бота'),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='author', description='Автор')
    ]
    await bot.set_my_commands(commands)

if __name__ == '__main__':
    loop = asyncio.get_event_loop() 
    loop.create_task(set_commands())

    executor.start_polling(
        dp, 
        loop=loop,
        skip_updates=True
    )