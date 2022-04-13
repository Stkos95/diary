from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tg_bot.keyboards.callbackdatas import diary_callback


diaryActionChooce = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="Добавить упражнение 🔥", callback_data=diary_callback.new(action="add_exercise"))
    ],
    [
        InlineKeyboardButton(text="Добавить тренировку 🎉", callback_data=diary_callback.new(action="add_training"))
    ]
])