from string import punctuation
from pymystem3 import Mystem

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command

from kbds import reply

user_private_router = Router()

@user_private_router.message((F.text.lower() == 'start') | (F.text.lower() == 'старт'))
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помощник', reply_markup=reply.start_kb)

@user_private_router.message((F.text.lower() == 'menu') | (F.text.lower() == 'меню'))
@user_private_router.message(Command('menu'))
async def menu_cmd(message: types.Message):
    await message.answer("Вот меню:")

@user_private_router.message((F.text.lower() == 'help') | (F.text.lower() == 'помощь'))
@user_private_router.message(Command('help'))
async def menu_cmd(message: types.Message):
    await message.answer("Вызов помощи!")

@user_private_router.message((F.text.lower() == 'lmao') | (F.text.lower() == 'лмао'))
@user_private_router.message(Command('lmao'))
async def popopo_cmd(message: types.Message):
    await message.answer("AYY LMAO")


def clean_text(text: str):
    return text.translate(str.maketrans('','',punctuation))


keywords_collection = [
    ['эдукон','едукон','educon','эдьюсон'],
    ['армия', 'призыв', 'отсрочка'],
    ['жужелица'],
]

answers_collection = ["Ответ по едукону","Ответ по армии","*жужжание*"]

lemmatizer = Mystem()

@user_private_router.message()
async def magic_cmd(message: types.Message):
    print("message:",message.text)
    text1 = ''.join(lemmatizer.lemmatize(message.text.lower()))
    text2 = message.text.lower()
    print("lemm:",text1)
    print("lower:",text2)
    isAnswered = False
    for i in range (0, len(keywords_collection)):
        if any(keyword in text1 for keyword in keywords_collection[i]) or any(keyword in text2 for keyword in keywords_collection[i]):
            await message.answer(answers_collection[i])
            isAnswered = True
    if isAnswered == False:
        await message.answer("Я тебя не понимаю")



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
