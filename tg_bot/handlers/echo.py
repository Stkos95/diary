from aiogram import types, Dispatcher
from table_class import Table
from tg_bot.config import load_config
from aiogram.dispatcher import FSMContext
from tg_bot.states import CreateTable, ShareTable, AppendExercice
from tg_bot.services.table import workTable

config = load_config(".env")
CREDENTIALS_FILE = "tg_bot\services\credentials1.json"



async def bot_echo(message: types.Message):
    await message.answer(message.text)



async def bot_create(message: types.Message, state: FSMContext):
    await message.answer("Вы выбрали команду 'Создать таблицу'")
    await message.answer("Укажи название документа:")
    await CreateTable.state_1.set()


async def bot_create_1(message: types.Message, state: FSMContext):
    nameDoc = message.text
    async with state.proxy() as data:
        data["nameDoc"] = nameDoc
    await message.answer("Как назвать первую вкладку?")
    await CreateTable.next()


async def bot_create_2(message: types.Message, state: FSMContext):
    nameTab = message.text
    async with state.proxy() as data:
        data["nameTab"] = nameTab
    created = workTable.create_table(title_doc=data["nameDoc"], title_sheet=data["nameTab"])
    await message.answer("Поздравляю, файл создан!\nДля пользования документом нужно открыть доступ.")

    await state.finish()


async def bot_share(message: types.Message):
    await message.answer(f"Вы нажали поделиться файлом:\nЕсли вы хотите поделиться файлом с id={workTable.spreadsheetId}, то укажите только электронную почту."
                         f"Если вы хотите поделиться другим документом, то укажите его id через запятую")
    await message.answer("Укажите электронную почту")
    await ShareTable.first()

async def bot_share_1(message: types.Message, state: FSMContext):
    text = message.text
    text.split(",")
    if len(text) > 1:
        email, spreadsheetId = text[0], text[1]
        workTable.shareToWritingMode(email,spreadsheetId)
    else:
        email = text[0]
        workTable.shareToWritingMode(email)
    await state.finish()


async def bot_add_spreadsheet_by_hand(message: types.Message):
    spreadsheetId = "1vuBudyT9AIV0tSMXwq8y3z3Tb1xlCSB61SPZfjmazBU"
    workTable.addDocbyHands(spreadsheetId=spreadsheetId)
    await message.answer("Ты добавил документ вручную!")


async def get_url(message: types.Message):
    link = workTable.getSheetLink()
    await message.answer(link)






def register_create(dp: Dispatcher):
    dp.register_message_handler(bot_echo, commands='hello', state=None)
    dp.register_message_handler(bot_create, commands='create', state=None)
    dp.register_message_handler(bot_create_1, state=CreateTable.state_1)
    dp.register_message_handler(bot_create_2, state=CreateTable.state_2)
    dp.register_message_handler(bot_share, commands='share', state=None)
    dp.register_message_handler(bot_share_1, state=ShareTable.state_1)
    dp.register_message_handler(bot_add_spreadsheet_by_hand, commands="add", state=None)
    dp.register_message_handler(get_url, commands='link')


