from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from aiogram import types, Dispatcher
from tg_bot.keyboards.callbackdatas import diary_callback, append_training_callback
from tg_bot.keyboards.trainkb import diaryActionChooce
from tg_bot.states import CreateTable, ShareTable, AppendExercice, AppendTraining
from tg_bot.services.table import workTable
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




async def start_func(message: types.Message):
    await message.answer(text="Выберите нужное:", reply_markup=diaryActionChooce)

async def append_exercice(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    await call.message.answer("Укажите отдельными сообщениями наименование упражнений")
    async with state.proxy() as data:
        data["exercise"] = []
    await AppendExercice.first()


async def append_training(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    kb = InlineKeyboardMarkup(row_width=1)
    exercises = workTable.getListOfExercises()
    for key, value in exercises.items():
        if value != []:
            kb.insert(InlineKeyboardButton(text=value[0], callback_data=append_training_callback.new(str(key))))
    await call.message.answer("Выбери упражнение, которое выполнил:", reply_markup=kb)
    await AppendTraining.first()

async def append_training_1(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    await call.message.answer("Укажите количество: ")
    ex_cell = workTable.findValueInCell(workTable.spreadsheetId)[:1]
    cellToAdd = f"{ex_cell}{callback_data['cell']}"
    async with state.proxy() as data:
        data["cellToAdd"] = cellToAdd
    await AppendTraining.first()

async def append_training_2(message: types.Message, state: FSMContext):
    value = message.text
    async with state.proxy() as data:
        workTable.addTraining(value, data["cellToAdd"])
        await message.answer("Успешно добавлен подход")
    await AppendTraining.state_1.set()

async def append_training_3(message: types.Message, state: FSMContext):
    await message.answer("Тренировка записана")
    await state.finish()



    # await call.message.answer("выберите упражнение из списка:")
    # async with state.proxy() as data:
    #     data["action"] = callback_data["action"]
    #     data["exercise"] = []
    #     print(data["action"])
    # await AppendExercice.first()


async def append_exercice_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["exercise"].append([message.text])

async def append_exercice_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # if data["action"] == "add_exercise":
        workTable.addExercice(data["exercise"])
        # elif data["action"] == "add_training":
        #     workTable.addTraining(data["exercise"])

    await message.answer("Готово")
    await state.finish()






def register_start(dp: Dispatcher):
    dp.register_message_handler(start_func, CommandStart())
    dp.register_callback_query_handler(append_exercice, diary_callback.filter(action="add_exercise"), state=None)
    dp.register_callback_query_handler(append_training, diary_callback.filter(action="add_training"), state=None)
    dp.register_callback_query_handler(append_training_1, append_training_callback.filter(), state=AppendTraining.state_1)
    dp.register_message_handler(append_training_3, text="Готово",state=AppendTraining.state_1 )
    dp.register_message_handler(append_training_2, state=AppendTraining.state_1)
    dp.register_message_handler(append_exercice_2, text="Готово",state=AppendExercice.state_1 )

    dp.register_message_handler(append_exercice_1, state=AppendExercice.state_1)