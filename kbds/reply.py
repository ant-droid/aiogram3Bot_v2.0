from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню")
        ],
        [
            KeyboardButton(text="Помощь")
        ],
        [
            KeyboardButton(text="LMAO")
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)