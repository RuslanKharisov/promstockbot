# handlers/onboarding.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from config import CHANNEL_LINK, CHANNEL_USERNAME
from keyboards.main_menu import get_main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, bot):
    user_id = message.from_user.id
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status not in ("member", "administrator", "creator"):
            await message.answer(
                f"📢 Для использования бота нужно быть подписанным на наш канал:\n\n{CHANNEL_LINK}\n\n"
                "После подписки нажмите /start"
            )
            return
    except Exception:
        await message.answer(
            f"❗ Не удалось проверить подписку. Подпишитесь вручную:\n\n{CHANNEL_LINK}\n\n"
            "Затем снова нажмите /start"
        )
        return

    await message.answer(
        f"Привет, <b>{message.from_user.full_name}</b>! Я бот для поставщиков Prom-Stock.\n\n"
        "Выберите действие:",
        reply_markup=get_main_menu()
    )

