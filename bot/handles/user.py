import random

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified, BadRequest

from pyqiwip2p import QiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime

from bot.handles.states import BalanceRefill
from bot.keyboards.keyboards import KeyboardManager
from bot.models.role import UserRole
from models.schemas import Bill
from bot.services.repository import Repo


async def start(m: Message, repo: Repo, db, logger, config, state: FSMContext):
    await m.reply(f'Привет, {m.from_user.first_name}')
    await m.bot.send_message(m.chat.id,
                             '🤑Я - бот для пополнения баланса.🤑 \n\n')
    user = await repo.get_user(m.from_user.id)
    await m.bot.send_message(m.chat.id,
                             f'👋{m.from_user.first_name} твой баланс {user.balance}₽ 💰\n\n👇Нажмите на кнопку снизу, чтобы пополнить баланс👇',
                             reply_markup=KeyboardManager.start_inline())
    return


async def refill_balance(cb: CallbackQuery, repo: Repo, db, logger, config, state: FSMContext):
    await cb.bot.answer_callback_query(cb.id, 'Waiting for ', show_alert=False)
    await cb.message.edit_text('Enter amount to top-up', reply_markup=KeyboardManager.waiting_amount_refill())
    await BalanceRefill.waiting_amount.set()
    return


async def user_back(cb: CallbackQuery, repo: Repo, db, logger, config, state: FSMContext):
    user = await repo.get_user(cb.from_user.id)

    await state.finish()
    await state.reset_data()

    await cb.bot.send_message(cb.message.chat.id,
                              f'👋{cb.from_user.first_name} твой баланс {user.balance}₽ 💰\n\n👇Нажмите на кнопку снизу, чтобы пополнить баланс👇',
                              reply_markup=KeyboardManager.start_inline())
    await cb.bot.answer_callback_query(cb.id, 'BACK ', show_alert=False)
    return


async def waiting_sum_refill(m: Message, repo: Repo, db, logger, config, state: FSMContext, p2p: QiwiP2P):
    sum = m.text
    await m.delete()
    # await m.bot.delete_message(m.chat.id, m.message_id - 1)
    if sum.isdigit():
        sum = int(sum)
        bill = p2p.bill(amount=sum, lifetime=15, comment=m.from_user.id + random.randint(1, 9999))
        db.add(Bill(id=m.from_user.id, billID=bill.bill_id, amount=sum))
        await m.bot.send_message(m.chat.id, f'💳💵 Pay with this url {bill.pay_url} 💳💵',
                                 reply_markup=KeyboardManager.pay_wait(bill.pay_url, bill.bill_id))
        logger.info(
            f'Создан счет #{bill.bill_id} на сумму {sum} для пользователя {m.from_user.id}')
    else:
        await m.bot.send_message(m.chat.id, '👇 Enter valid amount to top-up 👇')


async def update_balance(cb: CallbackQuery, repo: Repo, db, logger, config, state: FSMContext, p2p: QiwiP2P):
    update_data = cb.data
    bill_id = cb.data.split('_')[1]
    check = p2p.check(bill_id)
    if check.status == 'PAID':
        user = await repo.get_user(cb.from_user.id)
        cur_balance = user.balance
        new_balance = cur_balance + check.amount
        await repo.change_balance(cb.from_user.username, new_balance)
        await cb.bot.send_message(cb.message.chat.id,
                                  f'👋{cb.from_user.first_name} твой баланс {new_balance}₽ 💰\n\n👇Нажмите на кнопку снизу, чтобы пополнить баланс👇',
                                  reply_markup=KeyboardManager.start_inline())

    else:
        await cb.bot.answer_callback_query(cb.id, "🔄 Wait a few minutes and try again 🔄", show_alert=True)


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*', role=(UserRole.USER, UserRole.ADMIN))
    dp.register_callback_query_handler(refill_balance, lambda c: c.data == 'refill_balance', state='*',
                                       role=(UserRole.USER, UserRole.ADMIN))
    dp.register_message_handler(waiting_sum_refill, state=BalanceRefill.waiting_amount,
                                role=(UserRole.USER, UserRole.ADMIN))
    dp.register_callback_query_handler(user_back, lambda c: c.data == 'user_back', state='*',
                                       role=(UserRole.USER, UserRole.ADMIN))
    dp.register_callback_query_handler(update_balance, lambda c: c.data.find('update-balance_'), state='*',
                                       role=(UserRole.USER, UserRole.ADMIN))
