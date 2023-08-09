import random

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from src.main import dp
from src.main import active_sessions
from src.bot import keyboards

from src.parser.TabSession import TabSession
from src.parser.VacanciesContainer import VacanciesContainer
from src.parser.Vacancy import Vacancy

from src.bot.states import StorageStates


@dp.message_handler(commands=['start'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    mes = await message.answer('Зачекайте будь ласка...')

    # Check if user have active session, if not, creates new session
    if message.from_user.id in active_sessions.keys():
        session: TabSession = active_sessions[message.from_user.id]
        session.open_homepage()
    else:
        session = TabSession()
        active_sessions.update({message.from_user.id: session})

    await mes.edit_text('Вітаю у боті для пошуку вакансій на DOU JOBS',
                        reply_markup=await keyboards.start_options_markup())

    await state.set_state(StorageStates.basic_state)


@dp.callback_query_handler(keyboards.start_options_cd.filter(), state=StorageStates.basic_state)
async def start_cb_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    session: TabSession = active_sessions[call.from_user.id]

    # indicates what option user has chosen
    choice: str = callback_data.get('choice')

    match choice:
        case 'categories':
            await call.message.edit_text('Оберіть категорію',
                                         reply_markup=await keyboards.categories_markup(session.get_categories()))
        case 'search':
            session.open_homepage()

            await call.message.answer('Введіть ваш текстовий запит')
            await state.set_state(StorageStates.entering_request)


# Button "Пошук вручну" handler
@dp.message_handler(state=StorageStates.entering_request)
async def user_request_handler(message: types.Message, state: FSMContext):
    await message.answer('Робимо запит...')

    session: TabSession = active_sessions[message.from_user.id]
    session.send_request(message.text)

    vacs_container = session.download_vacancies()
    msg = vacs_container.get_formatted_vacancy_msg()

    if msg:
        await state.update_data({'vacs_container': vacs_container})
        await message.answer(msg,
                             reply_markup=await keyboards.vacancy_keyboard(),
                             disable_web_page_preview=True)
        await state.set_state(StorageStates.basic_state)
    else:
        await message.answer('Не знайдено вакансій')


# categories_markup callback handler
# categories selection
@dp.callback_query_handler(keyboards.category_cd.filter(), state=StorageStates.basic_state)
async def category_cb_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):

    # Deletes old keyboard
    # await call.message.edit_reply_markup(None)

    # Gets data from keyboard and saves to state dict
    cb_value = callback_data.get('category_value')
    await state.update_data({'category_value': cb_value})

    session: TabSession = active_sessions[call.from_user.id]
    session.set_category(cb_value)

    await call.message.edit_text('Оберіть рівень досвіду')
    await call.message.edit_reply_markup(await keyboards.exps_markup(session.get_exps()))


# exps_markup callback handler
# experience selection
@dp.callback_query_handler(keyboards.exp_cd.filter(), state=StorageStates.basic_state)
async def exp_cb_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    cb_text: str = callback_data.get('exp_text')
    await state.update_data({'exp_text': cb_text})

    session: TabSession = active_sessions[call.from_user.id]
    session.set_exp(cb_text)

    if cb_text.strip() == 'Без досвіду':
        markup = await keyboards.newbie_markup()
        await call.message.edit_text('Для початківців розрахований окремий розділ.\n'
                                  'Ви можете переглянути курси/стажування, або подивитися вакансії для початківців.'
                                  ' Нажаль, ці вакансії не поділяються за категоріями.')
        await call.message.edit_reply_markup(reply_markup=markup)
    else:
        markup = await keyboards.cities_markup(session.get_cities())
        if markup:
            await call.message.edit_text('Оберіть місто')
            await call.message.edit_reply_markup(await keyboards.cities_markup(session.get_cities()))
        else:
            await call.message.edit_text('Не знайдено вакансій')
            try:
                await call.message.edit_reply_markup(None)
            except Exception:
                pass


# cities_markup callback handler
# city selection
@dp.callback_query_handler(keyboards.city_cd.filter(), state=StorageStates.basic_state)
async def city_cb_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    cb_text = callback_data.get('city_text')
    await state.update_data({'city_text': cb_text})

    session: TabSession = active_sessions[call.from_user.id]
    session.set_city(cb_text)

    await call.message.edit_text('Завантаження вакансій...')
    vacs_container = session.download_vacancies()
    await state.update_data({'vacs_container': vacs_container})

    await call.message.edit_text(vacs_container.get_formatted_vacancy_msg(),
                                 reply_markup=await keyboards.vacancy_keyboard(),
                                 disable_web_page_preview=True)


# vacancy_markup callback handler
# navigation in vacancy menu
# functions: show next or previous vacancies, close menu
@dp.callback_query_handler(keyboards.vacancy_cd.filter(), state=StorageStates.basic_state)
async def vacancy_cb_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    choice: str = callback_data.get('choice')
    if_fjes = callback_data.get('if_fjes')

    if choice != 'cancel':
        session: TabSession = active_sessions[call.from_user.id]

        state_data = await state.get_data()

        if if_fjes == "True":
            vacs_container: VacanciesContainer = state_data['fjes_container']
        else:
            vacs_container: VacanciesContainer = state_data['vacs_container']

        # shows next vacancy
        if choice == 'show_following':
            vacancy_msg = vacs_container.get_formatted_vacancy_msg(following=True)
        # shows previous vacancy
        elif choice == 'show_previous':
            vacancy_msg = vacs_container.get_formatted_vacancy_msg(following=False)
        else:
            vacancy_msg = None

        if vacancy_msg:
            await call.message.edit_text(vacancy_msg, disable_web_page_preview=True)
            await call.message.edit_reply_markup(await keyboards.vacancy_keyboard())

            await state.update_data({'vacs_container': vacs_container})
            await call.answer()
        else:
            await call.answer(text='Далі немає вакансій')
    else:
        await call.message.edit_reply_markup(None)

    await call.answer()


# newbie_markup callback handler

# Dou has another section for "no experience" users. It has vacancies for newbies and events for newbies
# vacancies and events in this section don't divide into categories
@dp.callback_query_handler(keyboards.newbie_cd.filter(), state=StorageStates.basic_state)
async def newbie_kb_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    choice: str = callback_data.get('choice')

    session: TabSession = active_sessions[call.from_user.id]

    if choice == 'vacancies':
        await call.message.edit_text('Завантаження вакансій...')
        vacs_container = session.download_vacancies()
        await state.update_data({'vacs_container': vacs_container})

        await call.message.edit_text(vacs_container.get_formatted_vacancy_msg(), disable_web_page_preview=True)
        await call.message.edit_reply_markup(await keyboards.vacancy_keyboard())

    elif choice == 'events':
        await call.message.edit_text('Завантаження курсів і стажувань...')
        fjes_container = session.download_fjes()
        await state.update_data({'fjes_container': fjes_container})

        await call.message.edit_text(fjes_container.get_formatted_vacancy_msg(), disable_web_page_preview=True)

        await call.message.edit_reply_markup(await keyboards.vacancy_keyboard(fjes=True))










