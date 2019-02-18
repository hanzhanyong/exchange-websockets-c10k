# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

from websocket import create_connection
import time
import json

if __name__ == '__main__':
    while True:
        try:
            ws = create_connection(
                "wss://ws.kraken.com",
                http_proxy_host="127.0.0.1",
                http_proxy_port=1087)
            break
        except Exception as ex:
            print('connect ws error,retry...{}'.format(ex))
            time.sleep(2)

    print('connect is started.')

    # 订阅 KLine 数据
    tradeStr = json.dumps({
        "event": "subscribe",
        "pair": ["XBT/EUR", "ETH/USD"],
        "subscription": {
            "name": "ohlc",
            "interval": 1
        }
    })

    ws.send(tradeStr)

    while (True):
        res = ws.recv()
        time.sleep(0.5)
        print(type(res), res)
        resJosn = json.loads(res)
        if "event" in resJosn and resJosn["event"] == "ping":
            resJosn["event"] = "pong"
            pong = json.dumps(resJosn)
            ws.send(pong)
