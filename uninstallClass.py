# coding=utf-8
from settings import settings


class uninstallClass(object):
    def logger(self):
        setting = settings()
        print("redis", setting.redis)
        print("rabbitmq", setting.rabbitmq)
