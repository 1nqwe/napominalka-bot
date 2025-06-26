import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from bot.handlers.user_handlers import router


logging.basicConfig(level=logging.INFO)

async def startup(dispatcher: Dispatcher):
    print('Bot is starting...')

async def shutdown(dispatcher: Dispatcher):
    print('Bot is shutting down...')

async def main():
    load_dotenv()
    bot = Bot(token = os.getenv('TG_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass