from aiogram import Bot, Dispatcher, types
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


async def send_channel_message():
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text="✅ Запустить бот",
            url="https://t.me/MyStockAsist2025bot?start=start"
        )]
    ])

    await bot.send_message(
        chat_id='@promstock',  # сюда вставь @имя_канала
        text="PromstockBot — бот для поиска товаров у поставщиков и интеграции с вашим складом.",
        reply_markup=keyboard
    )


if __name__ == "__main__":
    asyncio.run(send_channel_message())
