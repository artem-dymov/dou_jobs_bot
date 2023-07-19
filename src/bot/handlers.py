import random

from aiogram import types
from src.main import dp
from src.main import active_sessions
from src.bot import keyboards

from src.parser.TabSession import TabSession


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if message.from_user.id in active_sessions.keys():
        session = active_sessions[message.from_user.id]
    else:
        session = TabSession()
        active_sessions.update({message.from_user.id: session})
    await message.answer('Hello to DOU JOBS. Choose category',
                         reply_markup=await keyboards.categories_markup(session.get_categories()))


# categories_markup callback handler
@dp.callback_query_handler(keyboards.category_cd.filter())
async def category_callback(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup(None)
    cb_value = callback_data.get('value')

    print(cb_value)
    await call.answer()


@dp.callback_query_handler(keyboards.exp_cd.filter())
async def exp_callback(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup(None)
    cb_text = callback_data.get('text')

    await call.answer()


@dp.callback_query_handler(keyboards.city_cd.filter())
async def city_callback(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup(None)
    cb_text = callback_data.get('text')

    await call.answer()



