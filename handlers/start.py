# # handlers/start.py
# from aiogram import Router
# from aiogram.types import Message
# from aiogram.filters import CommandStart
# from keyboards.main_menu import get_main_menu
#
# router = Router()
#
#
# @router.message(CommandStart())
# async def cmd_start(message: Message):
#     await message.answer(
#         f"Привет, <b>{message.from_user.full_name}</b>! Я бот для поставщиков Prom-Stock.\n\n"
#         "Выберите действие:",
#         reply_markup=get_main_menu()
#     )
