# core.py
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")  # хранится в .env

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
