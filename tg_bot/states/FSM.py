from aiogram.dispatcher.filters.state import StatesGroup, State

class CreateTable(StatesGroup):
    state_1 = State()
    state_2 = State()

class ShareTable(StatesGroup):
    state_1 = State()
    state_2 = State()


class AppendExercice(StatesGroup):
    state_1 = State()
    state_2 = State()

class AppendTraining(StatesGroup):
    state_1 = State()
