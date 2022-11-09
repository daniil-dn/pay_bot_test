import dataclasses

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import CallbackQuery
from sqlalchemy.dialects.postgresql import insert
from bot.models.role import UserRole
from models.schemas import User, BlackList


class RoleMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, admin_ids: int):
        super().__init__()
        self.admin_ids = admin_ids

    async def pre_process(self, obj, data, *args):
        # TODO Check user in dp black list

        if not getattr(obj, "from_user", None):
            data["role"] = None
        elif obj.from_user.id in self.admin_ids:
            data["role"] = UserRole.ADMIN
        else:
            data["role"] = UserRole.USER

        id = obj.from_user.id
        username = obj.from_user.username

        await data['repo'].conn.execute(
            insert(User).values({"id": id, "username": username}).on_conflict_do_nothing())
        await data['repo'].conn.commit()
        block_id = await data['repo'].conn.get(BlackList, id)
        if block_id:
            if type(obj) is CallbackQuery:
                cb_id = obj.id
                await self.manager.bot.answer_callback_query(obj.id, 'You are in black list!', show_alert=True)
            else:
                await obj.reply('You are in black list!')
            data["role"] = UserRole.Ban
            return

    async def post_process(self, obj, data, *args):
        del data["role"]
