from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню")
        ],
        [
            KeyboardButton(text="Помощь")
        ],
        [
            KeyboardButton(text="Новый вопрос")
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

del_kb = ReplyKeyboardRemove()