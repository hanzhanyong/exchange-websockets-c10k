# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

from websocket import create_connection
import gzip
import time

if __name__ == '__main__':
    while True:
        try:
            ws = create_connection(
                "wss://api.huobi.pro/ws",
                http_proxy_host="127.0.0.1",
                http_proxy_port=1087)
            break
        except Exception as ex:
            print('connect ws error,retry...{}'.format(ex))
            time.sleep(2)

    print('connect is started.')

    # 订阅 KLine 数据
    tradeStr1 = '{"sub": "market.ethusdt.kline.1min","id": "id10"}'

    # 请求 KLine 数据
    # tradeStr='{"req": "market.ethusdt.kline.1min","id": "id10", "from": 1513391453, "to": 1513392453}'

    # 订阅 Market Depth 数据
    # tradeStr='{"sub": "market.ethusdt.depth.step5", "id": "id10"}'

    # 请求 Market Depth 数据
    # tradeStr='{"req": "market.ethusdt.depth.step5", "id": "id10"}'

    # 订阅 Trade Detail 数据
    # tradeStr='{"sub": "market.ethusdt.trade.detail", "id": "id10"}'

    # 请求 Trade Detail 数据
    # tradeStr='{"req": "market.ethusdt.trade.detail", "id": "id10"}'

    # 请求 Market Detail 数据
    # tradeStr='{"req": "market.ethusdt.detail", "id": "id12"}'

    # 订阅  Market Tickers 数据
    tradeStr = '{"sub": "market.tickers", "id": "id110"}'

    ws.send(tradeStr1)
    ws.send(tradeStr)
    while (True):
        compressData = ws.recv()
        res = gzip.decompress(compressData).decode('utf-8')

        print(res)

        if res[:7] == '{"ping"':
            ts = res[8:21]
            pong = '{"pong":' + ts + '}'
            ws.send(pong)
#
