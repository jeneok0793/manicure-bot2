from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def handle_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📝 Записаться"), types.KeyboardButton(text="📅 Мои записи")],
            [types.KeyboardButton(text="❌ Отменить запись")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Привет! 💅 Я помогу тебе записаться на маникюр.\nВыбери, что хочешь сделать:",
        reply_markup=keyboard
    )

