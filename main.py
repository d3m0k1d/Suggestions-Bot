import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, F
from handlers.start import router as start_router
from handlers.user import router as user_router

load_dotenv('.env')
token = os.getenv('token')

dp = Dispatcher()
bot = Bot(token=token)

dp.include_router(start_router)
dp.include_router(user_router)
logging.basicConfig(level=logging.INFO)

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
