from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from services.suppliers import get_suppliers
from services.stock import get_stocks_by_sku
from states import SearchState

from typing import Optional, TypedDict
from datetime import datetime

router = Router()
user_states = {}


class StockItem(TypedDict, total=False):
    sku: str
    description: str
    category: str
    manufacturer: str
    quantity: int
    supplier: str
    email: str
    siteUrl: Optional[str]

    newDeliveryQty1: Optional[str]
    newDeliveryQty2: Optional[str]
    newDeliveryDate1: Optional[datetime]
    newDeliveryDate2: Optional[datetime]


@router.message(F.text == "🤝 Как подключиться?")
async def request_handler(message: Message):
    user_states[message.from_user.id] = "awaiting_request"
    await message.answer(
        "Оставьте ваш номер телефона и вопрос по подключению API.\n\n"
        "Пример:\n"
        "+79161234567 Хочу подключить склад к API"
    )


@router.message(lambda msg: "Найти товар" in msg.text)
async def ask_for_sku(message: types.Message, state: FSMContext):
    await message.answer("Введите артикул (SKU), по которому хотите найти товар:",
                         # reply_markup=ReplyKeyboardRemove()
                         )
    await state.set_state(SearchState.waiting_for_sku)


@router.message(SearchState.waiting_for_sku)
async def process_sku(message: Message, state: FSMContext):
    print("📥 Обработчик process_sku сработал")

    sku = message.text.strip()
    await state.clear()

    await message.answer(f"Ищу данные по артикулу: {sku}... 🔄")

    suppliers = await get_suppliers()

    results = await get_stocks_by_sku(sku, suppliers)

    if not results:
        await message.answer("❌ К сожалению, по данному артикулу ничего не найдено.")
        return

    for stock in results:
        sku = stock.get("sku", "—")
        description = stock.get("description", "—")
        manufacturer = stock.get("manufacturer", "—")
        quantity = stock.get("quantity", 0)
        supplier = stock.get("supplier", "—")
        email = stock.get("email", "—")
        site_url = stock.get("siteUrl")

        delivery1_qty = stock.get("newDeliveryQty1")
        delivery2_qty = stock.get("newDeliveryQty2")

        delivery1_text = ""
        delivery2_text = ""

        if delivery1_qty:
            try:
                date = stock.get("newDeliveryDate1")
                date_str = date.strftime("%d.%m.%Y") if date else "—"
            except Exception:
                date_str = "—"
            delivery1_text = f"🚚 Поставка 1: {delivery1_qty} шт – {date_str}\n"

        if delivery2_qty:
            try:
                date = stock.get("newDeliveryDate2")
                date_str = date.strftime("%d.%m.%Y") if date else "—"
            except Exception:
                date_str = "—"
            delivery2_text = f"🚚 Поставка 2: {delivery2_qty} шт – {date_str}"

        site_line = f"\n🔗 Сайт: {site_url}" if site_url else ""

        stock_line = f"📦 В наличии: {quantity} шт\n" if quantity > 0 else "📦 Нет в наличии, только поставка\n"

        text = (
            f"🏷️ Артикул: {sku}\n"
            f"📃 Описание: {description}\n"
            f"🏭 Производитель: {manufacturer}\n"
            f"👤 Поставщик: {supplier}\n"
            f"📧 Email: {email}"
            f"{site_line}\n\n"
            f"{stock_line}"
            f"{delivery1_text}"
            
            f"{delivery2_text}"
        )

        await message.answer(text)