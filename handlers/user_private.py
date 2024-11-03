from aiogram import types, Router
from aiogram.filters import CommandStart, Command

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помощник')

@user_private_router.message(Command('menu'))
async def menu_cmd(message: types.Message):
    await message.answer("Вот меню:")

@user_private_router.message(Command('help'))
async def menu_cmd(message: types.Message):
    await message.answer("Вызов помощи!")

@user_private_router.message(Command('lmao'))
async def popopo_cmd(message: types.Message):
    await message.answer("OOOOO LMAO")

edu = ['эдукон','едукон','educon','эдьюсон']
@user_private_router.message()
async def educon_cmd(message: types.Message):
    text = message.text
    for i in edu:
        if i in text:
            await message.answer("educon answer")
            break