# main.py

import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram import F
from config import BOT_TOKEN
from handlers import router

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
