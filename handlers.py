from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Я бот для записи на маникюр 💅\nВыбери действие из меню ниже или напиши команду.")
