import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
import os

from config import BOT_TOKEN
from handlers import router

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router)

async def on_startup(_: web.Application):
    await bot.set_webhook("https://manicure-bot2.onrender.com")

async def main():
    app = web.Application()
    dp.startup.register(on_startup)
    dp.setup(app, bot=bot)
    await setup_application(app, dp)
    return app

if __name__ == "__main__":
    web.run_app(main())
