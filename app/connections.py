# В идеале можно для конфига использовать .env и starlette.сonfig, но этим можно пренебречь из-за скромности проекта

from typing import Optional  # https://stackoverflow.com/questions/51710037/how-should-i-use-the-optional-type-hint
from aioredis import Redis, create_redis_pool
import aiopg


class RedisConn:

    def __init__(self):
        self.redis: Optional[Redis] = None

    async def init_cache(self):
        self.redis = await create_redis_pool('redis://localhost:6379/0?encoding=utf-8')

    async def incr(self, key):
        return await self.redis.incr(key)

    async def get(self, key):
        return await self.redis.get(key)

    async def close(self):
        self.redis.close()
        await self.redis.wait_closed()


class PostgresConn:

    def __init__(self):
        self.conn = None
        self.cur = None

    async def init_conn(self):
        self.conn = await aiopg.connect(host="localhost",
                                        database="test_db",
                                        user="postgres",
                                        password="postgres")
        self.cur = await self.conn.cursor()

    async def execute(self, query_string):
        await self.cur.execute(query_string)

    async def close(self):
        await self.conn.close()


redis_conn = RedisConn()
pg_conn = PostgresConn()
