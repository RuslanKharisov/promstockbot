from aiogram.types import BotCommand


def get_commands():
    return [
        BotCommand(command="start", description="🔍 Начать"),
        BotCommand(command="subscribe", description="📢 Подписка на канал"),
        BotCommand(command="consult", description="📝 Заявка на консультацию"),
        # Можно будет добавить:
        # BotCommand(command="search", description="🔎 Найти товар"),
    ]
