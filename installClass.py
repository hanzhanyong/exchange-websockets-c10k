# coding=utf-8
from settings import settings


class installClass(object):
    def logger(self):
        # setting = settings()
        # print("redis", setting.redis)
        # print("rabbitmq", setting.rabbitmq)
        print(self.__class__.__name__)
