from aiogram import Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified, BadRequest

from bot.models.role import UserRole
from bot.services.repository import Repo
from bot.keyboards.keyboards import KeyboardManager


async def admin_command(m: Message, repo: Repo, db, logger, config):
    await m.reply(f'✌️Привет, {m.from_user.first_name} ✌️', reply_markup=KeyboardManager.admin_start_inline())
    return


async def all_log(cb: CallbackQuery, repo: Repo, db, logger, config):
    f = open('./log_all.log', 'r')
    await cb.bot.send_document(cb.message.chat.id, f)
    await cb.bot.answer_callback_query(cb.id, 'Log file sended', show_alert='False')
    return


async def err_log(cb: CallbackQuery, repo: Repo, db, logger, config):
    f = open('./log_errors.log', 'r')
    await cb.bot.send_document(cb.message.chat.id, f)
    await cb.bot.answer_callback_query(cb.id, 'Log file sended', show_alert='False')
    return


async def get_users(cb: CallbackQuery, repo: Repo, db, logger, config):
    await cb.bot.answer_callback_query(cb.id, 'Users List', show_alert='False')
    usrs = await repo.list_users_str()
    users_str = "\n".join(usrs)
    await cb.bot.send_message(cb.message.chat.id, f'---Users---\n\n{users_str}')
    return


async def ban_unban_menu(cb: CallbackQuery, repo: Repo, db, logger, config):
    await cb.bot.answer_callback_query(cb.id, 'ban_user', show_alert='False')

    return


async def ban_user(cb: CallbackQuery, repo: Repo, db, logger, config):
    pass


async def ban_user(cb: CallbackQuery, repo: Repo, db, logger, config):
    pass


def register_admin(db: Dispatcher):
    db.register_message_handler(admin_command, commands=['admin'], state='*', role=UserRole.ADMIN)
    db.register_callback_query_handler(all_log, lambda c: c.data == 'all_log', state='*', role=UserRole.ADMIN)
    db.register_callback_query_handler(err_log, lambda c: c.data == 'err_log', state='*', role=UserRole.ADMIN)
    db.register_callback_query_handler(get_users, lambda c: c.data == 'get_users', state='*', role=UserRole.ADMIN)
    db.register_callback_query_handler(ban_unban_menu, lambda c: c.data == 'Black_List', state='*', role=UserRole.ADMIN)
    db.register_callback_query_handler(ban_user, lambda c: c.data == 'ban_user', state='*', role=UserRole.ADMIN)
    db.register_callback_query_handler(unban_user, lambda c: c.data == 'uban_user', state='*', role=UserRole.ADMIN)
