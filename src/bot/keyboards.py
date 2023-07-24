from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram import types

category_cd: CallbackData = CallbackData('category_id', 'category_value')


async def categories_markup(categories: list[str]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for category in categories:
        markup.row(
            InlineKeyboardButton(text=category, callback_data=category_cd.new(category))
        )
    return markup


exp_cd: CallbackData = CallbackData('exp_id', 'exp_text')


async def exps_markup(exps: list[str]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for exp in exps:
        markup.row(
            InlineKeyboardButton(text=exp, callback_data=exp_cd.new(exp))
        )
    return markup


city_cd: CallbackData = CallbackData('city_id', 'city_text')


async def cities_markup(cities: list[str]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for city in cities:
        markup.row(
            InlineKeyboardButton(text=city, callback_data=city_cd.new(city))
        )
    return markup


