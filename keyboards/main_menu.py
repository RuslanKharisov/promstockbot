# keyboards/main_menu.py
# 🔹 Главное меню бота.
#
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🤝 Как подключиться?")],
            [KeyboardButton(text="🔎 Найти товар на складе")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Поле ввода данных"
    )
