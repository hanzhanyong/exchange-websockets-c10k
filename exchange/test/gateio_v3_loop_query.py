# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

from websocket import create_connection
import requests
import time
import json
import sys
# API URL
# https://gateio.io/docs/futures/ws/index.html#candlesticks-subscription

def 

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('USE: python gateio.py [usd|eth]')

    symbolFlag = sys.argv[1] if len(sys.argv) > 1 else "usdt"

    symbolUrl = "https://data.gateio.io/api2/1/pairs"
    res = requests.get(symbolUrl)
    symbols = res.json()
    print(symbols)

    while True:
        try:
            ws = create_connection(
                # "wss://fx-ws-testnet.gateio.io/v4/ws",
                "wss://ws.gate.io/v3/",
                http_proxy_host="127.0.0.1",
                http_proxy_port=1087)
            break
        except Exception as ex:
            print('connect ws error,retry...{}'.format(ex))
            time.sleep(5)

    print('connect is started.')

    # 订阅 KLine 数据

    sub_data_list = [
        json.dumps({
            "id":
            int(time.time()),
            "method":
            "kline.query",
            "params":
            [symbol.upper(),
             int(time.time()) - 60,
             int(time.time()), 60]
        }) for symbol in symbols if symbol.endswith(symbolFlag.upper())
    ]

    print("sub_data_list", len(sub_data_list))
    #     ws.send(sub)
    sendIndex = 0
    startTime = time.time()
    ws.send(sub_data_list[sendIndex])
    # symbols_Events = []
    # symbols_Data_List = {}
    while True:
        res = ws.recv()
        resJson = json.loads(res)
        # print(resJson)

        sendIndex += 1

        if sendIndex >= 50:  # len(sub_data_list):
            sendIndex = 0
            endTime = time.time()
            print("end-start={}".format(endTime - startTime))
            startTime = endTime

        ws.send(sub_data_list[sendIndex])
