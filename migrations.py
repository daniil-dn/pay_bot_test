import asyncio

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.engine.url import URL

from bot.config import load_config

config = load_config("bot/bot.ini")
DATABASE = {
    'drivername': 'postgresql+asyncpg',  # Тут можно использовать MySQL или другой драйвер
    'host': config.db.host,
    'port': config.db.port,
    'username': config.db.user,
    'password': config.db.password,
    'database': config.db.database
}


def main():
    # Создаем объект Engine, который будет использоваться объектами ниже для связи с БД
    # engine = create_engine(URL.create(**DATABASE))
    engine = create_async_engine(URL.create(**DATABASE))
    from models.schemas import Base

    # Метод create_all создает таблицы в БД , определенные с помощью  DeclarativeBase
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init_models())


if __name__ == "__main__":
    main()
