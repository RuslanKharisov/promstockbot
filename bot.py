# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers import start, request
from handlers.subscribe import register_subscribe_handlers
from aiogram.fsm.storage.memory import MemoryStorage
storage = MemoryStorage()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)

# Регистрируем роутеры
dp.include_routers(
    start.router,
    request.router,
)

# Регистрируем подписку отдельно с доступом к bot
register_subscribe_handlers(dp, bot)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
