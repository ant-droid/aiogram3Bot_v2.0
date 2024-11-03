from string import punctuation

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command

user_private_router = Router()

@user_private_router.message((F.text.lower() == 'start') | (F.text.lower() == 'старт'))
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помощник')

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

edu = {'эдукон','едукон','educon','эдьюсон'}
army = {'арми', 'призыв', 'отсрочка'}

@user_private_router.message()
async def magic_cmd(message: types.Message):
    print(message.text)
    text = clean_text(message.text.lower().replace(" ",""))
    print(text)
    if any(keyword in text for keyword in edu):
        await message.answer("Ответ по едукону")
    elif any(keyword in text for keyword in army):
        await message.answer("Ответ по армии")


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
