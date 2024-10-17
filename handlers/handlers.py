from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database.vip import get_subscription_end, check_subscription
from kb import profile_kb, start_kb, buy_search

router = Router()



@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(f'<a href="https://telegra.ph/file/2ea1982b8f645208e5c03.jpg"><b>Nihao!</b></a> <b>Я osint-бот канала underllife.t.me</b>\n\n'
                     f'Ты можешь искать по:\n'
                     f'├ <b>Telegram ID:</b> <code>1183978425</code>\n'
                     f'├ <b>Phone number:</b> <code>+79000000000</code>\n'
                     f'├ <b>Fio:</b> <code>Александр Белов</code>\n'
                     f'├ <b>Mail:</b> <code><a href="mailto:osint@underlife.test">osint@underlife.test</a></code>\n'
                     f'├ <b>Address:</b> <code>Пушкина 69</code>\n'
                     f'├ <b>VKontakte:</b> <code><a href="https://vk.com/durov">https://vk.com/durov</a></code>\n'
                     f'├ <b>Username:</b> <code>underlife</code>'
                     , parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=await start_kb())
    await check_subscription(msg.from_user.id)


@router.message(F.text)
async def search(msg: Message):
    prem_text = (
        "📞Телефон:  79183440386\n"
        "📆Последняя активность:  1647526270298\n"
        "📆Дата регистрации:  2022-03-17 21:11:02.000\n"
        "🌃Код города:  435\n"
        "👤ФИО:  Peredriy Aleksey Vladimirovich\n"
        "📝Тип (физ/юр):  fiz\n\n"
        "📞Телефон:  79183440386\n"
        "📆Последняя активность:  1647526270298\n"
        "📆Дата регистрации:  2022-03-17 21:11:02.000\n"
        "🌃Код города:  435\n"
        "👤ФИО:  Передрий Алексей Владимирович\n"
        "📝Тип (физ/юр):  fiz\n\n"
        "📞Телефон:  79183440386\n"
        "🏘️АдресID:  1121803558\n"
        "🏭Название компании:  Передрий Алексей Владимирович\n"
        "👤ФИО:  Передрий Алексей Владимирович\n"
        "📌Код точки:  KSD6\n\n"
        "📞Телефон:  79183440386\n"
        "🏘️АдресID:  1139150580\n"
        "🏭Название компании:  Передрий Алексей Владимирович\n"
        "👤ФИО:  Передрий Алексей Владимирович\n"
        "📌Код точки:  KSD6\n"
    )

    text = (
        "📞Телефон: найдено\n"
        "📆Последняя активность: найдено\n"
        "📆Дата регистрации: найдено\n"
        "🌃Код города: найдено\n"
        "👤ФИО: найдено\n"
        "📝Тип (физ/юр): найдено\n\n"
        "📞Телефон: найдено\n"
        "📆Последняя активность: найдено\n"
        "📆Дата регистрации: найдено\n"
        "🌃Код города: найдено\n"
        "👤ФИО: найдено\n"
        "📝Тип (физ/юр): найдено\n\n"
        "📞Телефон: найдено\n"
        "🏘️АдресID: найдено\n"
        "🏭Название компании: найдено\n"
        "👤ФИО: найдено\n"
        "📌Код точки: найдено\n\n"
        "📞Телефон: найдено\n"
        "🏘️АдресID: найдено\n"
        "🏭Название компании: найдено\n"
        "👤ФИО: найдено\n"
        "📌Код точки: найдено\n\n"
        "💎 Для отображения результатов приобретите подписку!"
    )
    if await check_subscription(msg.from_user.id):
        await msg.answer(text=prem_text)
    else:
        await msg.answer(text, reply_markup=await buy_search())


@router.callback_query(lambda call: call.data == "profile")
async def profile_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username or "Unknown"
    first_name = callback.from_user.first_name
    last_name = callback.from_user.last_name or ""

    subscription_info = await get_subscription_end(user_id)

    message_text = (
        f'<b>Профиль пользователя:</b>\n'
        f'├ <b>ID:</b> <code>{user_id}</code>\n'
        f'├ <b>Username:</b> <code>@{username}</code>\n'
        f'├ <b>Имя:</b> <code>{first_name} {last_name}</code>\n'
        f'├ <b>Подписка:</b> <code>{subscription_info}</code>\n'
    )

    await callback.bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=message_text,
        reply_markup=await profile_kb(),
        parse_mode="HTML"
    )
    await check_subscription(callback.from_user.id)

@router.callback_query(lambda call: call.data == "back")
async def back_handler(callback: CallbackQuery):
    await callback.message.edit_text(f'<a href="https://telegra.ph/file/2ea1982b8f645208e5c03.jpg"><b>Nihao!</b></a> <b>Я osint-бот канала underllife.t.me</b>\n\n'
                     f'Ты можешь искать по:\n'
                     f'├ <b>Telegram ID:</b> <code>1183978425</code>\n'
                     f'├ <b>Phone number:</b> <code>+79000000000</code>\n'
                     f'├ <b>Fio:</b> <code>Александр Белов</code>\n'
                     f'├ <b>Mail:</b> <code><a href="mailto:osint@underlife.test">osint@underlife.test</a></code>\n'
                     f'├ <b>Address:</b> <code>Пушкина 69</code>\n'
                     f'├ <b>VKontakte:</b> <code><a href="https://vk.com/durov">https://vk.com/durov</a></code>\n'
                     f'├ <b>Username:</b> <code>underlife</code>'
                     , parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=await start_kb())
    await check_subscription(callback.from_user.id)