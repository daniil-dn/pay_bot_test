import asyncpgx

from typing import List
from sqlalchemy import select

from models.schemas import User


async def create_pool(user, password, database, host, echo):
    pool = await asyncpgx.create_pool(database=database, user=user, password=password, host=host)
    return pool


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    async def get_username_from_id(self, user_id) -> str:
        req = f'select username from tg_users where user_id = {user_id}'
        res = await self.conn.fetch(req)
        username = res[0]['username']
        return username

    # users
    async def add_user(self, user_id, username) -> None:
        """Store user in DB, ignore duplicates"""
        request = f"INSERT INTO tg_users(user_id, username) VALUES ({user_id}, '{username}') ON CONFLICT DO NOTHING;"
        await self.conn.execute(
            request
        )
        return

    async def list_users_str(self) -> List[int]:
        """List all bot users"""
        # return await self.conn.fetch(
        #     f"select userid from tg_users;"
        # )
        res = await self.conn.execute(select(User))
        res = res.all()

        res = [f'{i[0].id}      -       {i[0].username}     -       🏦  {i[0].balance}' for i in res]
        return res

    async def list_listened_channel(self):
        '''List all channel which are listened by the bot'''

        request = 'select * from listened_channel_name;'

        res_list = [row[0] for row in await self.conn.fetch(request)]
        return res_list

    async def rm_listened_channel(self, channel_name):
        '''Remove a channel which are listened by the bot'''
        channel_name = channel_name.replace('/', '').replace('\\', '').replace('"', '').replace('\'', '')
        request = f"delete from listened_channel_name where channel_name='{channel_name}';"
        return await self.conn.execute(request)

    async def add_listened_channel(self, channel_name):
        '''Add a channel which are listened by the bot'''
        channel_name = channel_name.replace('/', '').replace('\\', '').replace('"', '').replace('\'', '')
        request = f"insert into listened_channel_name (channel_name) values ('{channel_name}') on conflict do nothing;"
        return await self.conn.execute(request)

    async def add_later_queue(self, vacancy_id, logger=None):
        if type(vacancy_id) is int:
            request = f"insert into later_queue (id) values ({vacancy_id}) on conflict do nothing"
            return await self.conn.execute(request)
        else:
            logger.error(f"{vacancy_id} - vacancy_id is not valid IN add_later_queue")
            return False

    async def add_tomorrow_queue(self, vacancy_id, logger=None):
        if type(vacancy_id) is int:
            request = f"insert into tomorrow_queue (id) values ({vacancy_id}) on conflict do nothing"
            return await self.conn.execute(request)
        else:
            logger.error(f"{vacancy_id} - vacancy_id is not valid IN add_tomorrow_queue")
            return False

    async def get_vacancy(self, vacancy_id, logger=None):

        request = f'select * from user_vacancies where id = {int(vacancy_id)} ;'

        res_list = [row for row in await self.conn.fetch(request)]
        return res_list

    async def ban_user(self, user_id):
        request = f"INSERT INTO ban_list (user_id) VALUES ({user_id}) ON CONFLICT DO NOTHING;"
        await self.conn.execute(
            request
        )
        return "user is banned"

    async def unban_user(self, user_id):
        request = f"delete from ban_list where user_id = {user_id};"
        await self.conn.execute(
            request
        )
        return "user is unbanned"

    async def banlist_str(self):
        request = f"select * from ban_list;"
        return str([row[0] for row in await self.conn.fetch(request)])

    async def check_ban(self, user_id) -> bool:
        return bool([
            row[0]
            for row in await self.conn.fetch(
                f"select user_id from ban_list where user_id = {user_id}",
            )
        ])

    async def write_vacancy(self, main_part, tags, link, userid) -> bool:
        try:
            main_part = main_part.replace("'", "''")
            tags = tags.replace("'", "''")
            link = link.replace("'", "''")
            request = fr"INSERT INTO user_vacancies(main_part, tags, link, date_time, user_id) VALUES " \
                      fr"('{main_part}', '{tags}', '{link}', CURRENT_TIMESTAMP, {userid}) ON CONFLICT DO NOTHING;"
            await self.conn.execute(
                request
            )
        except Exception as err:
            print(err)
            return False
        return True

# SELECT pg_xact_commit_timestamp(xmin) as time, * FROM tg_users order by time limit 1; #Check for update
