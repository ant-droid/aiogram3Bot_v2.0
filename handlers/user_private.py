from string import punctuation
from aiogram.enums import ParseMode
from aiogram.enums import ChatType
from pymystem3 import Mystem

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_questions
from filters.chat_types import ChatTypeFilter
from aiogram.utils.formatting import (
    as_list,
    as_marked_section,
    Bold,
)



from kbds import reply
from kbds.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))

@user_private_router.message((F.text.lower() == 'start') | (F.text.lower() == 'старт'))
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет, я виртуальный помощник",
        reply_markup=get_keyboard(
            "Меню",
            "Кнопка1",
            "Кнопка2",
            "Кнопка3",
            placeholder="Что вас интересует?",
            sizes=(1,1,1,1)
        ),
    )

@user_private_router.message((F.text.lower() == 'menu') | (F.text.lower() == 'меню'))
@user_private_router.message(Command('menu'))
async def menu_cmd(message: types.Message):
    await message.answer("Вот меню:")

@user_private_router.message((F.text.lower() == 'help') | (F.text.lower() == 'помощь'))
@user_private_router.message(Command('help'))
async def menu_cmd(message: types.Message):
    await message.answer("Вызов помощи!")

@user_private_router.message((F.text.lower() == 'new') | (F.text.lower() == 'новый вопрос'))
@user_private_router.message(Command('new'))
async def new_cmd(message: types.Message):
    await message.answer("Введите название нового вопроса:")
    answerName = message.text.lower()
    await message.answer("Введите ключевые слова:")
    splitting_keywords = message.text.lower().split()
    keywords_collection.append(splitting_keywords)
    await message.answer("Введите ответ для бота:")
    answers_collection.append( message.text.lower())






def clean_text(text: str):
    return text.translate(str.maketrans('','',punctuation))

answer_names = [
    "1","2","3"
]

keywords_collection = [
    ['эдукон','едукон','educon','эдьюсон'],
    ['армия', 'призыв', 'отсрочка'],
    ['жужелица'],
    ['документ', 'справка'],
    ['дирекция']

]

answers_collection = ["Ответ по едукону","Ответ по армии","*жужжание*","ответ по документам и справкам","ответ по дирекции"]

lemmatizer = Mystem()

@user_private_router.message(F.text)
async def magic_cmd(message: types.Message, session: AsyncSession):
    print("message:",message.text)
    text1 = ''.join(lemmatizer.lemmatize(message.text.lower()))
    text2 = message.text.lower()
    print("lemm:",text1)
    print("lower:",text2)

    isAnswered = False
    for question in await orm_get_questions(session):
        keywords_list = [k.strip() for k in question.keywords.split(",")]
        """
        keywords_list_lemm = ''.join(lemmatizer.lemmatize(question.keywords.lower()))
        keywords_list.extend(keywords_list_lemm.split(","))
        """
        print(question.keywords," - ",keywords_list, "\n")
        if any(keyword in text1 for keyword in keywords_list) or any(keyword in text2 for keyword in keywords_list):
            if question.image is not None:
                await message.answer_photo(question.image, caption = question.description)
            else:
                await message.answer(question.description)
            isAnswered = True
    if isAnswered == False:
        await message.answer("<b>Я тебя не понимаю</b>")



"""
@user_private_router.message()
async def magic_cmd(message: types.Message):
    print(message.text)
    text = clean_text(message.text.lower().replace(" ",""))
    print(text)
    if any(keyword in text for keyword in edu):
        await message.answer("Ответ по едукону")
    elif any(keyword in text for keyword in army):
        await message.answer("Ответ по армии")
"""

'''
@user_private_router.message(lambda c: c.data in edu)
async def magic_cmd(message: types.Message):
    await message.answer("Это магический фильтр")
'''
"""
@user_private_router.message()
async def educon_cmd(message: types.Message):
    text = message.text
    for i in edu:
        if i in text:
            await message.answer("educon answer")
            break
"""
'''
@user_private_router.message(F.text.lower().contains("educon"))
async def magic_cmd(message: types.Message):
    await message.answer("Это магический фильтр")
'''

"""
isAnswered = False
    for question in await orm_get_questions(session):
        print(question.keywords, "\n")
    for i in range (0, len(keywords_collection)):
        if any(keyword in text1 for keyword in keywords_collection[i]) or any(keyword in text2 for keyword in keywords_collection[i]):
            await message.answer(answers_collection[i])
            isAnswered = True
    if isAnswered == False:
        await message.answer("<b>Я тебя не понимаю</b>")
"""