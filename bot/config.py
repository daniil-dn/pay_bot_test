import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list
    use_redis: bool
    channel_id: id


@dataclass
class Telethone:
    api_id: int
    api_hash: str
    to_forward: int


@dataclass
class Webhook:
    webhook_host: str
    webapp_host: str
    webapp_port: int


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes")


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]
    db = config["db"]

    # Для получения массива админов из конфига bot.ini
    admins = tg_bot["admin_ids"].replace(' ', '').split(',')
    # Проверка на правильно введеное id админов.
    admins = [i for i in admins if i.isalnum()]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            admin_ids=list(map(int, admins)),
            use_redis=cast_bool(tg_bot.get("use_redis")),
            channel_id=int()
        ),
        db=DbConfig(user=db['user'], password=db['password'], database=db['database'], host=db['host']),

    )