# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

import asyncio

import time
import datetime
import aiohttp
import json
import requests

PROXY = "http://127.0.0.1:1087"
URL = "https://api.hitbtc.com/api/2"

g_last_kline_list = {}


async def http_get_kline(session, url, symbol, proxy):
    global g_last_kline_list
    localUrl = "{}/public/candles/{}?period=M1&limit=2".format(
        URL, symbol.upper())
    startTime = time.time()
    while startTime + 1800 > time.time():
        async with session.get(localUrl, proxy=proxy) as response:
            response = await response.read()
            res = response.decode("utf-8")
            # print(res)
            """
            [{"timestamp":"2019-01-21T00:02:00.000Z","open":"0.99806798","close":"0.99200947","min":"0.99200947","max":"0.99806798","volume":"47","volumeQuote":"46.67028637"},{"timestamp":"2019-01-22T16:47:00.000Z","open":"1.00999999","close":"1.00999999","min":"1.00999999","max":"1.00999999","volume":"2","volumeQuote":"2.01999998"}]
            """
            resJson = json.loads(res)
            resJson = resJson[len(resJson) - 1]
            # print(resJson)
            # dtime = datetime.strptime(resJson["timestamp"], "%Y-%m-%d %H:%M:%S.%Z")
            lastKlineTime = int((datetime.datetime.strptime(
                resJson['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ') +
                                 datetime.timedelta(hours=8)).timestamp())
            # lastKlineTime = int(
            #     time.mktime(
            #         time.strptime(resJson["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%Z")))
            curKlineTime = int(time.time())
            # print(lastKlineTime, curKlineTime, lastKlineTime + 180 > curKlineTime)
            if (lastKlineTime + 60 > curKlineTime):

                if symbol not in g_last_kline_list:
                    g_last_kline_list[symbol] = {
                        "count": 1,
                        "timediff": curKlineTime - lastKlineTime
                    }
                else:
                    g_last_kline_list[symbol][
                        "count"] = 1 + g_last_kline_list[symbol]["count"]
                    g_last_kline_list[symbol][
                        "timediff"] = curKlineTime - lastKlineTime
                # print(len(g_last_kline_list))
                print(g_last_kline_list)


if __name__ == '__main__':

    url = "{}/public/symbol".format(URL)

    r = requests.get(url, proxies={'https': '127.0.0.1:1087'})
    # print(r.json())
    conn = aiohttp.TCPConnector(limit=0)  # 不限制连接池数量 默认100
    session = aiohttp.ClientSession(connector=conn)

    tasks = [
        http_get_kline(session, URL, symbol["id"].upper(), PROXY)
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
