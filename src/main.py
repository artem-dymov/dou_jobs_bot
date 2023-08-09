import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

with open('src/config.json', 'r') as file:
    data = json.load(file)
    bot_token = data['BOT_TOKEN']
    user_agent = data['USER_AGENT']
    chromedriver_location = data['CHROMEDRIVER_LOCATION']

bot = Bot(token=bot_token)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

active_sessions = {}

if __name__ == '__main__':
    from src.bot.handlers import dp
    executor.start_polling(dp, skip_updates=True)

