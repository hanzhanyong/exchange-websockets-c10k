# coding=utf-8
"""
local config
"""

from .base import *

redis = {"host": "127.0.0.1", "port": 6379, "db": 0, "password": "123456"}
rabbitmq = {
    'vhost': '/',
    'host': "127.0.0.1",
    "port": 5672,
    "user": "guest",
    "password": "guest"
}
