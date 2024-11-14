import asyncio
import os
import logging
from aiogram.client.bot import DefaultBotProperties
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy

from dotenv import load_dotenv
load_dotenv()

from handlers.user_private import user_private_router
###from handlers.user_messageRecognizer_private import user_messageRecognizer_private_router
from handlers.admin_private import admin_router
from common.bot_cmds_list import private

ALLOWED_UPDATES = ['message, edited_message']
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

bot.my_admins_list = [310999305]

dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(user_private_router)

###dp.include_router(user_messageRecognizer_private_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    #await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')



