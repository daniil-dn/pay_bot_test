from aiogram import Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified, BadRequest

from bot.keyboards.keyboards import KeyboardManager
from bot.models.role import UserRole
from bot.services.repository import Repo


async def start(m: Message):
    await m.reply(f'Привет, {m.from_user.first_name}')
    await m.bot.send_message(m.chat.id,
                             '🤑Я - бот для пополнения баланса.🤑 \n\n'
                             '👇Нажмите на кнопку снизу, чтобы пополнить баланс👇',
                             reply_markup=KeyboardManager.start_inline())
    return


async def refill_balance(cb: CallbackQuery, repo: Repo, db, logger, config):
    await cb.bot.answer_callback_query(cb.id, 'Update', show_alert='False')
    return


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*', role=(UserRole.USER, UserRole.ADMIN))
    dp.register_callback_query_handler(refill_balance, lambda c: c.data == 'refill_balance', state='*',
                                       role=(UserRole.USER, UserRole.ADMIN))
