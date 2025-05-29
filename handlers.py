from aiogram import Router, types

router = Router()

@router.message()
async def echo_message(message: types.Message):
    await message.answer("Бот работает. Напиши 'записаться', и я начну диалог (пока логика не подключена).")
