# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

import sys
import aiohttp
import asyncio

# import multiprocessing
# from multiprocessing import Process

import exchange


async def connectWs(ex):
    try:
        async with ex.connect() as ws:
            try:
                # dispatch
                await ex.subscribe()
                while True:
                    rdata = await ex.recev()
                    await ex.parse(rdata)

                await ex.close()
            # 其他错误
            except Exception as e:
                print(f'{ex.name}: recev error: {e}')
                await ws.close(ws)
                return
    except Exception as e:
        print(f'{ex.name} websocket connect error: {e}')
        return

    asyncio.sleep(2)  # delay 2 second

    # reconnect websocket
    await connectWs(ex)


async def processStart(exchangeList=[]):
    loop = asyncio.get_event_loop()
    conn = aiohttp.TCPConnector(limit=0)  # default 100
    session = aiohttp.ClientSession(connector=conn)

    tasks = []
    for exName in exchangeList:
        ex = getattr(exchange, exName)()
        ex.session = session
        tasks.append(connectWs(ex))

    loop.run_until_complete(asyncio.wait(tasks))
    loop.run_forever()


def mainStart(exchangeList=[]):
    # LOCAL_PROCESS_NUM = multiprocessing.cpu_count()
    # exchangeList = ["huobipro", "okex", "binance"]

    # p = Process(target=process_start,args=(url_list,))
    # p.start()
    processStart(exchangeList)
    # print("mainStart", exchangeList)


def mainInstall(exchangeList=[]):
    print("mainInstall", exchangeList)


def mainUnInstall(exchangeList=[]):
    print("mainUnInstall", exchangeList)


def mainStatics(exchangeList=[]):
    print("mainStatics", exchangeList)


def Usage():
    print('Usage:\n\
        python main.py [dev|prod|local] [install|uninstall|start|statics] [all|huobipro|okex|binance] \n\n\
    i.e python main.py local start all\n')


if __name__ == '__main__':
    # main_huobipro()
    # install uninstall run statics
    if len(sys.argv) < 4:
        Usage()
        exit(0)

    cmdName = sys.argv[2]
    exchangeName = sys.argv[3]

    exchangeList = []
    if exchangeName == "all":
        exchangeList = ["huobipro", "okex", "binance"]
    else:
        exchangeList = exchangeName.split("|")

    # check exchange is true
    for exchageName in exchangeList:
        try:
            ex = getattr(exchange, exchageName)()
            print(f"{exchageName} is OK!")
        except Exception as ex:
            print(ex)
            exit(0)

    if cmdName == "install":
        mainInstall(exchangeList)
    elif cmdName == "uninstall":
        mainUnInstall(exchangeList)
    elif cmdName == "start":
        mainStart(exchangeList)
    elif cmdName == "statics":
        mainStatics(exchangeList)
    else:
        print(f"{cmdName} command is not exists!")
        Usage()

    # myinstall = installClass()
    # myinstall.logger()
    # print(sys.argv)
