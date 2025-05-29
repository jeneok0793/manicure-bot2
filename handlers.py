from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот для записи. Напиши 'записаться', чтобы начать!")

@router.message()
async def fallback_handler(message: types.Message):
    await message.answer("Я пока не понял тебя 😅 Напиши 'записаться' — и я всё расскажу.")
