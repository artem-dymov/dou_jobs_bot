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

    for city in cities:
        markup.row(
            InlineKeyboardButton(text=city, callback_data=city_cd.new(city))
        )
    return markup


vacancy_cd = CallbackData('vacancy_id', 'choice')


async def vacancy_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='⬅️', callback_data=vacancy_cd.new('show_previous')),
        InlineKeyboardButton(text='➡️', callback_data=vacancy_cd.new('show_following'))
    )
    markup.row(
        InlineKeyboardButton(text='Відмінити', callback_data=vacancy_cd.new('cancel'))
    )

    return markup


