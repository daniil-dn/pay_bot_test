from aiogram import Dispatcher, types
from aiogram.types import Message
from aiogram.utils.exceptions import MessageNotModified, BadRequest

from bot.services.repository import Repo


async def start(m: Message):
    await m.reply('HI')
    return


def register_user(dp: Dispatcher):
    dp.register_message_handler(callback=start, commands=['start'], state='*')
