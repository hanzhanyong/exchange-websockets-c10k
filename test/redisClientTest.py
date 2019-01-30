# coding=utf-8
import sys
import os
import time
import unittest
import asyncio

# http://www.cnblogs.com/yajing-zh/p/6807968.html
curPath = os.getcwd()
father_path = os.path.abspath(os.path.dirname(curPath) + os.path.sep + ".")
sys.path.append(father_path)
# print(sys.path)

from utils.redisClient import redisClient
from settings import settings

# async def set(redisConfig, loop):
#     with redisClient(redisConfig) as redis:
#         await redis.set("mykey", "myname{}".format(time.time()))
#         value = await redis.get("mykey")
#         print(value)


class redisClientTest(unittest.TestCase):
    async def test_get(self):
        sConf = settings()
        redis = redisClient(sConf.redis)
        await redis.open()
        value = await redis.get("mykey")
        self.assertEqual(value, 'value')
        await redis.close()

    async def test_set(self):
        sConf = settings()
        redis = redisClient(sConf.redis)
        await redis.open()
        value = "myname{}".format(int(time.time()))
        await redis.set("mykey", value)
        valueNew = await redis.get("mykey")
        self.assertEqual(value, valueNew)
        await redis.close()

    # def test_get(self):
    #     sConf = settings()
    #     redis = redisClient(sConf.redis)
    #     redis.open()
    #     value = redis.get("mykey")
    #     self.assertEqual(value, 'value')
    #     redis.close()

    # def test_set(self):
    #     sConf = settings()
    #     redis = redisClient(sConf.redis)
    #     redis.open()
    #     value = "myname{}".format(int(time.time()))
    #     redis.set("mykey", value)
    #     valueNew = redis.get("mykey")
    #     self.assertEqual(value, valueNew)
    #     redis.close()

    # def test_key(self):
    #     d = redisClient()
    #     d['key'] = 'value'
    #     self.assertEqual(d.key, 'value')


if __name__ == '__main__':
    unittest.main()
