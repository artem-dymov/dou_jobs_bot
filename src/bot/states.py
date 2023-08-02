from aiogram.dispatcher.filters.state import State, StatesGroup


class StorageStates(StatesGroup):
    basic_state = State()
    entering_request = State()

