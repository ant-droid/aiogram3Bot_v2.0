import asyncio
import os
import logging

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv
load_dotenv()

from handlers.user_private import user_private_router

ALLOWED_UPDATES = ['message, edited_message']
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(BOT_TOKEN)

dp = Dispatcher()

dp.include_router(user_private_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')



