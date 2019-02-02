# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

import aiohttp
import asyncio
import requests
import aiohttp
import time
import json
import sys
# API URL
# https://gateio.io/docs/futures/ws/index.html#candlesticks-subscription

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}


async def getsource(session, url):
    # print(url)
    res = requests.get(symbolUrl)
    print(res)
    # async with session.get(url) as req:  # 获得请求
    #     if req.status == 200:  # 判断请求码

    #         print(req.data)
    #     else:
    #         print("访问失败")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('USE: python gateio.py [usd|eth]')

    symbolFlag = sys.argv[1] if len(sys.argv) > 1 else "usdt"

    symbolUrl = "https://data.gateio.io/api2/1/pairs"
    res = requests.get(symbolUrl)
    symbols = res.json()
    print(symbols)
    startTime = time.time()

    loop = asyncio.get_event_loop()

    conn = aiohttp.TCPConnector(limit=0, verify_ssl=False)  # 防止ssl报错
    session = aiohttp.ClientSession(connector=conn)
    tasks = [
        getsource(
            session,
            "https://api.bibox.com/v1/mdata?cmd=kline&pair={}&period=1min&size=1"
            .format(symbol)) for symbol in symbols
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    endTime = time.time()
    print("end-start={}".format(endTime - startTime))
