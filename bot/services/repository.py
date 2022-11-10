import asyncpgx

from typing import List
from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert

from models.schemas import User, BlackList


async def create_pool(user, password, database, host, echo):
    pool = await asyncpgx.create_pool(database=database, user=user, password=password, host=host)
    return pool


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn, logger):
        self.conn = conn
        self.logger = logger

    async def list_users_str(self) -> List[int]:
        """List all bot users with balance"""
        res = await self.conn.execute(select(User))
        res = res.all()

        res = [f'{i[0].id}      -       {i[0].username}     -       🏦  {i[0].balance}' for i in res]
        return res

    async def ban_user(self, user_data) -> Exception | bool:
        # TODO сделать бан по username
        try:
            await self.conn.execute(
                insert(BlackList).values({"id": user_data, }).on_conflict_do_nothing())
            await self.conn.commit()
            return True
        except Exception as err:
            self.logger.error(err)
            return err

    async def unban_user(self, user_data) -> Exception | bool:
        # TODO сделать разбан по username
        try:
            await self.conn.execute(
                delete(BlackList).where(BlackList.id == user_data))
            await self.conn.commit()
            return True
        except Exception as err:
            self.logger.error(err)
            return err

    async def change_balance(self, username: str, balance: int) -> bool:
        try:
            await self.conn.execute(
                update(User).where(User.username == username).values(balance=balance)
            )
            await self.conn.commit()
            return True
        except Exception as err:
            self.logger.error(err)
            return False

    async def get_user(self, userID):
        res = await self.conn.get(User, int(userID))
        return res
