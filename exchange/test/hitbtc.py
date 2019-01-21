# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

from websocket import create_connection
# import gzip
import sys
import time
import json

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('USE: python hitbtc.py btc_usdt,eth_usdt')

    symbols = sys.argv[1] if len(sys.argv) > 1 else "btc_usdt"
    symbols = symbols.split(",")

    while True:
        try:
            ws = create_connection(
                "wss://api.hitbtc.com/api/2/ws",
                http_proxy_host="127.0.0.1",
                http_proxy_port=1087)
            break
        except Exception as ex:
            print('connect ws error,retry...{}'.format(ex))
            time.sleep(2)

    print('connect is started.')

    try:
        # 订阅  Market Kline 数据
        sub_data_list = []
        subId = 10000
        for symbol in symbols:
            subId += 1
            subData = json.dumps({
                "method": "subscribeCandles",
                "params": {
                    "symbol": symbol.replace("_", "").upper(),
                    "period": "M1",
                    "limit": 1
                },
                "id": subId
            })
            sub_data_list.append(subData)

        print(sub_data_list)

        for sub in sub_data_list:
            ws.send(sub)

        # ping = json.dumps({"method": "server.ping", "params": [], "id": 100})
        # timeStart = time.time()
        while True:
            res = ws.recv()

            # timeEnd = time.time()
            # if timeEnd - timeStart > 0.5:  # 2 seconds ping heartbeat
            #     timeStart = timeEnd
            #     ws.send(ping)
            print(res)

    except Exception as ex:
        print(ex)
