from aiogram.dispatcher.filters.state import State, StatesGroup


class StorageStates(StatesGroup):
    basic_state = State()
    # add entering_data state and stat when user entered all data
