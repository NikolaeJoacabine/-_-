import json
import logging
import bot_db
import asyncio
from aiogram import Bot, Dispatcher
from telegram import handlers
from dotenv import dotenv_values
import pika

config = dotenv_values(".env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    bot_db.create_db()
    BOT_TOKEN = config["BOT_TOKEN"]

    bot = Bot(token="7985787217:AAFyHwZsHfQigij2u41ymyxF_XfuDFP7Nn8")
    dp = Dispatcher()

    dp.include_router(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
