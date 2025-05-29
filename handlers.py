# handlers.py

from aiogram import Router, types
from config import ADMIN_CHAT_ID

router = Router()

@router.message(commands=["start"])
async def start_handler(message: types.Message):
    if message.from_user.id == ADMIN_CHAT_ID:
        await message.answer("Добро пожаловать, админ!")
    else:
        await message.answer("Привет! Я бот для записи 🧴💅")
