# coding=utf-8
"""
dev config
"""

from .base import *

redis = {"host": "127.0.0.1", "port": 6379, "db": 0, "password": "dev"}
rabbitmq = {
    'vhost': '/',
    'host': "127.0.0.1",
    "port": 5672,
    "user": "guest",
    "password": "dev"
}
