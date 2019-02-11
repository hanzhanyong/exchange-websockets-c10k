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

    async def open(self, exchangeName='', queueName='hello', callback=None):
        try:
            self.transport, self.protocol = await aioamqp.connect(
                host=self.config["host"],
                port=self.config["port"],
                login=self.config["user"],
                password=self.config["password"],
                virtualhost=self.config["vhost"],
                loop=self.loop)
            self.channel = await self.protocol.channel()

            # await self.channel.queue_declare(
            #     queue_name=queueName, durable=True)
            await self.channel.queue_declare(queue_name=queueName)

            if callback:
                await self.channel.basic_qos(
                    prefetch_count=1, prefetch_size=0, connection_global=False)
                await self.channel.basic_consume(
                    callback, queue_name=queueName)

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
        await self.channel.basic_publish(
            payload=msg,
            exchange_name=self.exchangeName,
            routing_key=self.queueName)

    # async def receiveMessage(self, channel, body, envelope, properties):
    #     print(" [x] Received %r" % body)
    #     await asyncio.sleep(body.count(b'.'))


"""
---------------------TEST----------------------------
"""

sConfig = {
    'vhost': '/',
    'host': "127.0.0.1",
    "port": 5672,
    "user": "guest",
    "password": "guest"
}


async def exampleSend(loop):

    amqp = amqpClient(sConfig, loop)
    opened = await amqp.open()
    # print(opened)
    if opened is True:
        numIndex = 0
        while True:
            await amqp.sendMessage("test time {}".format(time.time()))
            numIndex += 1
            if numIndex == 1000:
                break

        await amqp.close()


async def mycallback(channel, body, envelope, properties):
    await asyncio.sleep(0.01)
    print(" [x] Received %r" % body)
    # print(" [x] Done")
    await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)


async def worker(loop):
    amqp = amqpClient(sConfig, loop)
    opened = await amqp.open(callback=mycallback)
    # print(opened)
    if opened is True:
        print("opened is ok")
    else:
        print("opened is error")


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(exampleSend(loop))
    # event_loop.run_forever()

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(worker(event_loop))
    event_loop.run_forever()
