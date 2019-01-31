# coding=utf-8
import asyncio
import aioamqp
import time


class amqpClient(object):
    """
    redis Client
    """

    def __init__(self, mqConfig, loop=None):
        self.config = mqConfig
        self.loop = loop

        self.transport = None
        self.protocol = None
        self.channel = None
        self.exchangeName = None
        self.queueName = None

    async def open(self, exchangeName='', queueName='hello'):
        try:
            self.transport, self.protocol = await aioamqp.connect(
                host=self.config["host"],
                port=self.config["port"],
                login=self.config["user"],
                password=self.config["password"],
                virtualhost=self.config["vhost"],
                loop=self.loop)
            self.channel = await self.protocol.channel()
            await self.channel.queue_declare(queue_name=queueName)
            self.exchangeName = exchangeName
            self.queueName = queueName
        except Exception as ex:
            self.pool = None
            print(ex)
            return False
        return True

    async def close(self):
        if self.protocol is None:
            return
        await self.protocol.close()
        self.transport.close()

    async def sendMessage(self, msg):
        await channel.basic_publish(
            payload=msg, exchange_name='', routing_key='hello')

    async def receiveMessage(self, msg):
        print(msg)


"""
---------------------TEST----------------------------
"""

from .settings import settings


async def exampleSend(loop):
    sConfig = settings()
    amqp = amqpClient(sConfig.rabbitmq, loop)
    opened = await amqp.open()
    if opened is True:
        while 
        amqp.sendMessage("test{}".format(time.time()))

        amqp.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(exampleSend(loop))
