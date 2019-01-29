# coding=utf-8
"""
init config
"""
import sys
from enum import Enum, unique


@unique
class SettingEnum(Enum):
    DEV = "dev"
    LOCAL = "local"
    PROD = "prod"


class settings(object):
    def __init__(self):
        """
        init
        """
        argv = sys.argv
        self._content = dict()
        if len(argv) >= 2:
            settingType = sys.argv[1]
        # print("settingType", settingType, SettingEnum.DEV.value)
        if settingType == SettingEnum.PROD.value:
            from .prod import redis, rabbitmq
        elif settingType == SettingEnum.DEV.value:
            from .dev import redis, rabbitmq
        else:
            from .local import redis, rabbitmq

        self._content["redis"] = redis
        self._content["rabbitmq"] = rabbitmq

    def __del__(self):
        self._content.clear()

    def __getitem__(self, item):
        return self._content.get(item, None)

    def __setitem__(self, key, value):
        self._content[key] = value
        return value

    def __getattr__(self, item):
        return self._content.get(item, None)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        self._content[key] = value
        return value
