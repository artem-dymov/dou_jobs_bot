from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram import types
from typing import Union
from src.parser.Vacancy import Vacancy

start_options_cd = CallbackData('start_options_cd', 'choice')


async def start_options_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Категорії', callback_data=start_options_cd.new('categories'))
    )
    markup.row(
        InlineKeyboardButton(text='Пошук вручну', callback_data=start_options_cd.new('search'))
    )
    return markup

category_cd = CallbackData('category_id', 'category_value')


async def categories_markup(categories: list[str]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for category in categories:
        markup.row(
            InlineKeyboardButton(text=category, callback_data=category_cd.new(category))
        )
    return markup


exp_cd = CallbackData('exp_id', 'exp_text')


async def exps_markup(exps: list[str]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Не обирати', callback_data=exp_cd.new('*'))
    )
    for exp in exps:
        markup.row(
            InlineKeyboardButton(text=exp, callback_data=exp_cd.new(exp))
        )
    return markup


city_cd = CallbackData('city_id', 'city_text')


async def cities_markup(cities: list[str]) -> Union[InlineKeyboardMarkup, None]:
    markup = InlineKeyboardMarkup()

    if not cities:
        return None

    markup.row(
        InlineKeyboardButton(text='Не обирати', callback_data=city_cd.new('*'))
    )
    for city in cities:
        markup.row(
            InlineKeyboardButton(text=city, callback_data=city_cd.new(city))
        )

    return markup


vacancy_cd = CallbackData('vacancy_id', 'choice', 'if_fjes')


# if fjes attribute is True, it means that this keyboard will be used for newbie events (JobFirstEvent objects)
async def vacancy_keyboard(fjes=False):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='⬅️', callback_data=vacancy_cd.new('show_previous', str(fjes))),
        InlineKeyboardButton(text='➡️', callback_data=vacancy_cd.new('show_following', str(fjes)))
    )
    markup.row(
        InlineKeyboardButton(text='Відмінити', callback_data=vacancy_cd.new('cancel', str(fjes)))
    )

    return markup


newbie_cd = CallbackData('newbie_id', 'choice')

# This markup will be called when user presses the button "Без досвіду"
async def newbie_markup():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Курси та івенти', callback_data=newbie_cd.new('events')),
        InlineKeyboardButton(text='Вакансії', callback_data=newbie_cd.new('vacancies'))
    )

    return markup
