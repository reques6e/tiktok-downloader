from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import _config

bot = Bot(
    token=_config['API_TOKEN'], 
    parse_mode='HTML',
    disable_web_page_preview=True
)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)