import aiogram
import logging

from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot.handles.user import register_user
from bot.services.repository import create_pool
from bot.config import load_config

logfile = 'log_bot.log'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

FH = logging.FileHandler(logfile)
basic_formater = logging.Formatter('%(asctime)s : [%(levelname)s] : %(message)s')
FH.setFormatter(basic_formater)
logger.addHandler(FH)


async def on_startup(dp):
    # client = TelegramClient("test", 10582137, 'bcc45c276f0c29e35cc5d56422c60e45')
    # await client.start()

    config = load_config("bot/bot.ini")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # logger.error("Starting bot")
    # if config.tg_bot.use_redis:
    #     storage = RedisStorage2()
    # else:
    #     storage = MemoryStorage()

    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
        echo=False,
    )

    # dp.middleware.setup(DbMiddleware(pool))
    # dp.middleware.setup(EnvironmentMiddleware(config, logger, client))
    # dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_ids))
    # dp.filters_factory.bind(RoleFilter)
    # dp.filters_factory.bind(AdminFilter)
    #
    # register_admin(dp)
    register_user(dp)


if __name__ == '__main__':
    token = '5221121872:AAHiIxuyZl8-lYqN33rq7BddlfgTNbMw8kg'
    bot = aiogram.Bot(token=token)
    dp = aiogram.Dispatcher(bot=bot, storage=RedisStorage2())
    aiogram.executor.start_polling(dp, on_startup=on_startup)
