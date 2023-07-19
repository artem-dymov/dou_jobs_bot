import json
from aiogram import Bot, Dispatcher, executor, types

with open('src/config.json', 'r') as file:
    bot_token = json.load(file)['BOT_TOKEN']

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

active_sessions = {}

if __name__ == '__main__':
    from src.bot.handlers import dp
    executor.start_polling(dp, skip_updates=True)

