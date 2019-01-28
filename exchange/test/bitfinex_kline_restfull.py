# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

import asyncio

import time
import aiohttp
import json
import requests

PROXY = "http://127.0.0.1:1087"
URL = "https://api.bitfinex.com/v2/candles"

g_last_kline_list = []


async def http_get_kline(session, url, symbol, proxy):
    global g_last_kline_list
    async with session.get(
            "{}/trade:1m:t{}/last".format(url, symbol.upper()),
            proxy=proxy) as response:
        response = await response.read()
        res = response.decode("utf-8")
        # print(res)
        resJson = json.loads(res)
        lastKlineTime = int(resJson[0] / 1000)
        curKlineTime = int(time.time())
        # print(lastKlineTime, curKlineTime, lastKlineTime + 180 > curKlineTime)
        if (lastKlineTime + 60 > curKlineTime):
            symbolState = [
                symbol, lastKlineTime, curKlineTime,
                lastKlineTime + 60 > curKlineTime
            ]
            print(symbolState)
            g_last_kline_list.append(symbolState)


if __name__ == '__main__':

    url = "https://api.bitfinex.com/v1/symbols"
    r = requests.get(url, proxies={'https': '127.0.0.1:1087'})

    conn = aiohttp.TCPConnector(limit=0)  # 不限制连接池数量 默认100
    session = aiohttp.ClientSession(connector=conn)

    tasks = [
        http_get_kline(session, URL, symbol.upper(), PROXY)
        for symbol in r.json()
    ]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    print(len(g_last_kline_list), g_last_kline_list)

    a = input("are you exit app? y | n")
    if a.lower() == "y":
        loop.close()
    else:
        loop.close()
    # loop.close()
