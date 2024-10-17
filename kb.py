from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def start_kb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="👤 Профиль", callback_data="profile"))
    return builder.as_markup()


async def profile_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💎 Купить подписку", callback_data="buy"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))
    return builder.as_markup()

async def buy_search():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💎 Купить подписку", callback_data="buy"))
    return builder.as_markup()

async def buy_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="7 дней 160р", callback_data="vbuy:7:160"))
    builder.row(InlineKeyboardButton(text="Месяц 400р", callback_data="vbuy:30:400"))
    builder.row(InlineKeyboardButton(text="Год 2000р", callback_data="vbuy:365:2000"))
    return builder.as_markup()


async def payment(invoice, price, duration):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=f"💰 Оплатить {price}р", url=f"{invoice.bot_invoice_url}"))
    builder.row(InlineKeyboardButton(text="💳 Я оплатил", callback_data=f"check_pay:{invoice.invoice_id}:{duration}"))
    return builder.as_markup()