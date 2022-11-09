from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from bot.services.repository import Repo


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, pool, logger):
        super().__init__()
        self.pool = pool
        self.logger = logger

    async def pre_process(self, obj, data, *args):
        db = self.pool()
        data["db"] = db
        data["repo"] = Repo(db, self.logger)

    async def post_process(self, obj, data, *args):
        del data["repo"]
        db = data.get("db")
        if db:
            await db.close()
