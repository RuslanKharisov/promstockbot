# handlers/api_request.py
# 🔹 Обрабатывает "🤝 Как подключиться?" и валидацию.
#
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.api_request import ApiRequestState
from utils.validators import extract_phone, extract_email
from utils.sheets import append_to_sheet

router = Router()


@router.message(F.text == "🤝 Как подключиться?")
async def request_handler(message: Message, state: FSMContext):
    await state.set_state(ApiRequestState.waiting_for_contact)
    await message.answer(
        "Оставьте ваш номер телефона или email и вопрос по подключению API.\n\n"
        "Пример:\n"
        "+79161234567 Хочу подключить склад к API"
    )


@router.message(ApiRequestState.waiting_for_contact)
async def handle_api_request(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text.strip()

    phone = extract_phone(text)
    email = extract_email(text)

    if not phone and not email:
        await message.answer(
            "❗ Пожалуйста, укажите корректный номер телефона (например, +79991234567) "
            "или email (например, user@example.com)."
        )
        return

    append_to_sheet(user_id, username, text)
    await state.clear()

    await message.answer(
        f"✅ Спасибо! Мы получили ваш запрос:\n\n{text}\n\n"
        "Свяжемся с вами в ближайшее время."
    )

