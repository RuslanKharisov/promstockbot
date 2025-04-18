from aiogram import Router, F
from aiogram.types import Message
from config import CHANNEL_LINK, CHANNEL_USERNAME

router = Router()


def register_subscribe_handlers(router: Router, bot):
    @router.message(F.text == "📢 Подписаться на канал")
    async def subscribe_handler(message: Message):
        user_id = message.from_user.id
        try:
            member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
            if member.status in ("member", "administrator", "creator"):
                await message.answer(f"✅ Вы подписаны на канал: {CHANNEL_LINK}")
            else:
                await message.answer(f"Подпишитесь на канал: {CHANNEL_LINK}")
        except Exception:
            await message.answer(f"❗ Не удалось проверить подписку. Просто подпишитесь вручную: {CHANNEL_LINK}")
