from aiogram import Router
from aiogram.types import CallbackQuery

from database.vip import add_or_update_subscription
from kb import buy_kb, payment

from aiocryptopay import AioCryptoPay, Networks

crypto = AioCryptoPay(token='15314:AA11PvpdsOCl2WgpSpeqvfQohuaSETFCJEa', network=Networks.TEST_NET)

vip_router = Router()

@vip_router.callback_query(lambda call: call.data == "buy")
async def payment_handler(callback: CallbackQuery):
    await callback.message.answer("📆 Выберите на сколько будете покупать подписку:", reply_markup=await buy_kb())


@vip_router.callback_query(lambda call: call.data.startswith("vbuy"))
async def buy_vip(callback: CallbackQuery):
    duration = callback.data.split(":")[1]
    price = callback.data.split(":")[2]
    invoice = await crypto.create_invoice(amount=int(price), fiat='RUB', currency_type='fiat')
    await callback.bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="💸 Оплатите чек, после оплаты нажмите кнопку 'Я оплатил'!",
        reply_markup=await payment(
            invoice=invoice,
            price=price,
            duration=duration
        )
    )


@vip_router.callback_query(lambda call: call.data.startswith("check_pay"))
async def check_payment(callback: CallbackQuery):
    invoice_id = callback.data.split(":")[1]
    duration = callback.data.split(":")[2]

    invoice_status = await crypto.get_invoices(invoice_ids=int(invoice_id))

    if invoice_status.status == "paid":
        await add_or_update_subscription(user_id=callback.from_user.id, duration=int(duration))
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="✅ Оплата подтверждена! Ваша подписка активирована."
        )
    else:
        await callback.answer(
            "❌ Оплата не найдена или ещё не завершена. Попробуйте позже или проверьте статус оплаты.")