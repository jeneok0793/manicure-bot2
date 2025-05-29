import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiohttp import web

from config import BOT_TOKEN, WEBHOOK_URL
from handlers import router
from google_sheets import init_google_sheets

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(router)

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info("Webhook set")
    await init_google_sheets()

async def on_shutdown(app):
    logging.info("Shutting down...")
    await bot.delete_webhook()

async def handle(request):
    body = await request.read()
    update = bot.session.json_loads(body)
    await dp.feed_update(bot, update)
    return web.Response()

app = web.Application()
app.router.add_post("/", handle)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    web.run_app(app, port=10000)
