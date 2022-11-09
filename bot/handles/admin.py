from aiogram import Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified, BadRequest

from bot.handles.states import Ban_Unban_state, BalanceChange
from bot.models.role import UserRole
from bot.services.repository import Repo
from bot.keyboards.keyboards import KeyboardManager


async def text_handler(m: Message, repo: Repo, db, logger, config):
    await m.reply(f'✌✌️')
    return


async def admin_command(m: Message, repo: Repo, db, logger, config, state):
    await state.reset_data()
    await m.reply(f'✌️Привет, {m.from_user.first_name} ✌️', reply_markup=KeyboardManager.admin_start_inline())
    return


async def all_log(cb: CallbackQuery, repo: Repo, db, logger, config):
    f = open('./log_all.log', 'r')
    await cb.bot.send_document(cb.message.chat.id, f)
    await cb.bot.answer_callback_query(cb.id, 'Log file sended', show_alert=False)
    return


async def err_log(cb: CallbackQuery, repo: Repo, db, logger, config):
    f = open('./log_errors.log', 'r')
    await cb.bot.send_document(cb.message.chat.id, f)
    await cb.bot.answer_callback_query(cb.id, 'Log file sended', show_alert=False)
    return


async def get_users(cb: CallbackQuery, repo: Repo, db, logger, config):
    await cb.bot.answer_callback_query(cb.id, 'Users List', show_alert=False)
    usrs = await repo.list_users_str()
    users_str = "\n".join(usrs)
    await cb.bot.send_message(cb.message.chat.id, f'---Users---\n\n{users_str}',
                              reply_markup=KeyboardManager.admin_start_inline())
    return


async def ban_unban_menu(cb: CallbackQuery, repo: Repo, db, logger, config):
    await cb.bot.answer_callback_query(cb.id, 'ban_user', show_alert=False)
    await cb.bot.edit_message_textedit_message_reply_markup(cb.message.chat.id, message_id=cb.message.message_id,
                                                            reply_markup=KeyboardManager.ban_unban_menu())
    return


async def back_ban_unban_menu(cb: CallbackQuery, repo: Repo, db, logger, config, state):
    await state.finish()
    await state.reset_data()
    await cb.bot.answer_callback_query(cb.id, 'Back', show_alert=False)

    await cb.bot.edit_message_textedit_message_reply_markup(cb.message.chat.id, message_id=cb.message.message_id,
                                                            reply_markup=KeyboardManager.admin_start_inline())
    return


async def ban_user(cb: CallbackQuery, repo: Repo, db, logger, config, state):
    await cb.bot.answer_callback_query(cb.id, text='Enter user id')
    await cb.bot.edit_message_textedit_message_reply_markup(cb.message.chat.id, message_id=cb.message.message_id,
                                                            reply_markup=KeyboardManager.ban_enter())
    await state.update_data(message_id=cb.message.message_id)
    await Ban_Unban_state.waiting_for_ban_id.set()


async def waiting_ban_user(m: Message, repo: Repo, db, logger, config, state):
    state_data = await state.get_data()
    message_id = state_data['message_id']
    username = 'username'
    userID = 0

    await m.delete()

    await m.bot.edit_message_text(f'{username} - {userID} UNBANED', m.chat.id,
                                  message_id=message_id,
                                  reply_markup=KeyboardManager.admin_start_inline())
    await Ban_Unban_state.waiting_for_ban_id.set()


async def unban_user(cb: CallbackQuery, repo: Repo, db, logger, config, state):
    await cb.bot.answer_callback_query(cb.id, text='Enter user id')
    await cb.bot.edit_message_textedit_message_reply_markup(cb.message.chat.id, message_id=cb.message.message_id,
                                                            reply_markup=KeyboardManager.unban_enter())
    await state.update_data(message_id=cb.message.message_id)
    await Ban_Unban_state.waiting_for_unban_id.set()


async def waiting_unban_user(m: Message, repo: Repo, db, logger, config, state: FSMContext):
    state_data = await state.get_data()
    message_id = state_data['message_id']
    username = 'username'
    userID = 0
    await m.delete()

    await m.bot.edit_message_text(f'{username} - {userID} UNBANED', m.chat.id,
                                  message_id=message_id, reply_markup=KeyboardManager.admin_start_inline())
    await state.finish()


async def change_balance(cb: CallbackQuery, repo: Repo, db, logger, config, state):
    await cb.bot.answer_callback_query(cb.id, text='Enter userID or username')
    await cb.bot.edit_message_text('Waiting for userID or username', cb.message.chat.id,
                                   message_id=cb.message.message_id,
                                   reply_markup=KeyboardManager.balance_userid_enter())
    await state.update_data(message_id=cb.message.message_id)
    await BalanceChange.waiting_user.set()


async def waiting_user_balance(m: Message, repo: Repo, db, logger, config, state: FSMContext):
    state_data = await state.get_data()
    message_id = state_data['message_id']
    username = 'username'
    userID = 0
    await m.delete()
    await m.bot.edit_message_text('Waiting for a new balance', m.chat.id,
                                  message_id=message_id,
                                  reply_markup=KeyboardManager.balance_amount_enter(username))

    await state.update_data(username=username, userID=userID)
    await BalanceChange.waiting_amount.set()


async def waiting_amount_balance(m: Message, repo: Repo, db, logger, config, state: FSMContext):
    state_data = await state.get_data()
    message_id = state_data['message_id']
    username = state_data['username']
    userID = state_data['userID']
    amount = m.text if m.text.isdigit() else None
    await m.delete()

    if amount:
        await m.bot.edit_message_text(f'{username} - {userID} changed to 💰 {amount}', m.chat.id,
                                      message_id=message_id,
                                      reply_markup=KeyboardManager.admin_start_inline())
    else:
        await m.bot.edit_message_text(f'Entered invalid {username} - {userID} ', m.chat.id,
                                      message_id=message_id,
                                      reply_markup=KeyboardManager.balance_amount_enter(username))
        await BalanceChange.waiting_amount()

    await state.finish()
    await state.reset_data()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_command, commands=['admin'], state='*', role=UserRole.ADMIN)
    dp.register_callback_query_handler(all_log, lambda c: c.data == 'all_log', state='*', role=UserRole.ADMIN)
    dp.register_callback_query_handler(err_log, lambda c: c.data == 'err_log', state='*', role=UserRole.ADMIN)
    dp.register_callback_query_handler(get_users, lambda c: c.data == 'get_users', state='*', role=UserRole.ADMIN)
    dp.register_callback_query_handler(ban_unban_menu, lambda c: c.data == 'black_List', state='*', role=UserRole.ADMIN)
    dp.register_callback_query_handler(back_ban_unban_menu, lambda c: c.data == 'black_List_back', state='*',
                                       role=UserRole.ADMIN)
    dp.register_callback_query_handler(ban_user, lambda c: c.data == 'ban_user', state='*', role=UserRole.ADMIN)
    dp.register_message_handler(waiting_ban_user, state=Ban_Unban_state.waiting_for_ban_id, role=UserRole.ADMIN)
    dp.register_callback_query_handler(unban_user, lambda c: c.data == 'unban_user', state='*', role=UserRole.ADMIN)
    dp.register_message_handler(waiting_unban_user, state=Ban_Unban_state.waiting_for_unban_id, role=UserRole.ADMIN)

    dp.register_callback_query_handler(change_balance, lambda c: c.data == 'change_balance', state='*',
                                       role=UserRole.ADMIN)
    dp.register_message_handler(waiting_user_balance, state=BalanceChange.waiting_user, role=UserRole.ADMIN)
    dp.register_message_handler(waiting_amount_balance, state=BalanceChange.waiting_amount, role=UserRole.ADMIN)
    dp.register_message_handler(text_handler, state="*")
