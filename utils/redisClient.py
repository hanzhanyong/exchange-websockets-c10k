# coding=utf-8
# import asyncio
import aioredis


class redisClient(object):
    """
    redis Client
    """

    def __init__(self, redisConfig, loop=None):
        self.config = redisConfig
        self.loop = loop
        self.pool = None

    # def __enter__(self):
    #     try:
    #         self.pool = aioredis.create_pool(
    #             "redis://{}".format(self.config["host"]),
    #             self.config["port"],
    #             db=self.config["db"],
    #             password=self.config["password"],
    #             loop=self.loop)
    #     except Exception as ex:
    #         self.pool = None
    #         print(ex)
    #     return self

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     if self.pool is not None:
    #         self.pool.close()
    #         self.pool.wait_closed()
    async def open(self):
        try:
            self.pool = await aioredis.create_pool(
                "redis://{}".format(self.config["host"]),
                self.config["port"],
                db=self.config["db"],
                password=self.config["password"],
                loop=self.loop)
        except Exception as ex:
            self.pool = None
            print(ex)
        return self

    async def close(self):
        if self.pool is None:
            return
        self.pool.close()
        await self.pool.wait_closed()

    async def set(self, key, value):
        if self.pool is None:
            return None
        result = await self.pool.execute("SET", key, value)
        return result

    async def get(self, key):
        if self.pool is None:
            return None
        value = await self.pool.execute("GET", key)
        return value
