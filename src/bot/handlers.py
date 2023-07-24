import random

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from src.main import dp
from src.main import active_sessions
from src.bot import keyboards

from src.parser.TabSession import TabSession

from src.bot.states import StorageStates


@dp.message_handler(commands=['start'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    mes = await message.answer('Зачекайте будь ласка...')

    # Check if user have active session, if not, creates new session
    if message.from_user.id in active_sessions.keys():
        session = active_sessions[message.from_user.id]
    else:
        session = TabSession()
        active_sessions.update({message.from_user.id: session})

    await mes.edit_text('Hello to DOU JOBS. Choose category',
                        reply_markup=await keyboards.categories_markup(session.get_categories()))

    await state.set_state(StorageStates.basic_state)


# categories_markup callback handler
@dp.callback_query_handler(keyboards.category_cd.filter(), state=StorageStates.basic_state)
async def category_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):

    # Deletes old keyboard
    # await call.message.edit_reply_markup(None)

    # Gets data from keyboard and saves to state dict
    cb_value = callback_data.get('category_value')
    await state.update_data({'category_value': cb_value})

    session: TabSession = active_sessions[call.from_user.id]
    session.set_category(cb_value)

    await call.message.edit_text('Оберіть рівень досвіду')
    await call.message.edit_reply_markup(await keyboards.exps_markup(session.get_exps()))


@dp.callback_query_handler(keyboards.exp_cd.filter(), state=StorageStates.basic_state)
async def exp_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    print('--1')

    cb_text = callback_data.get('exp_text')
    await state.update_data({'exp_text': cb_text})

    session: TabSession = active_sessions[call.from_user.id]
    session.set_exp(cb_text)

    await call.message.edit_text('Оберіть місто')
    await call.message.edit_reply_markup(await keyboards.cities_markup(session.get_cities()))


@dp.callback_query_handler(keyboards.city_cd.filter(), state=StorageStates.basic_state)
async def city_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    print('1')

    cb_text = callback_data.get('city_text')
    await state.update_data({'city_text': cb_text})

    session: TabSession = active_sessions[call.from_user.id]
    session.set_city(cb_text)

    await call.message.edit_reply_markup(None)




