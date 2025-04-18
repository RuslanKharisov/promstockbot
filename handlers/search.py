# handlers/search.py
# 🔹 Обрабатывает ввод SKU и выводит результат.
#

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.search import SearchState
from services.suppliers import get_suppliers
from services.stock import get_stocks_by_sku
from datetime import datetime

router = Router()


@router.message(lambda msg: "Найти товар" in msg.text)
async def ask_for_sku(message: Message, state: FSMContext):
    await message.answer("Введите артикул (SKU), по которому хотите найти товар:")
    await state.set_state(SearchState.waiting_for_sku)


@router.message(SearchState.waiting_for_sku)
async def process_sku(message: Message, state: FSMContext):
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
            date = stock.get("newDeliveryDate1")
            date_str = date.strftime("%d.%m.%Y") if isinstance(date, datetime) else "—"
            delivery1_text = f"🚚 Поставка 1: {delivery1_qty} шт – {date_str}\n"

        if delivery2_qty:
            date = stock.get("newDeliveryDate2")
            date_str = date.strftime("%d.%m.%Y") if isinstance(date, datetime) else "—"
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
