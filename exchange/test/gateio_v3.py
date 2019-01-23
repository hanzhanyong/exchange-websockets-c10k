# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

from websocket import create_connection
import time
import json
import sys
# API URL
# https://gateio.io/docs/futures/ws/index.html#candlesticks-subscription

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('USE: python gateio.py btc_usd,eth_usd')

    symbols = sys.argv[1] if len(sys.argv) > 1 else "btc_usd"
    symbols = symbols.split(",")

    # 订阅 KLine 数据

    # sub_data_list = [
    #     json.dumps({
    #         "time": int(time.time()),
    #         "channel": "futures.candlesticks",
    #         "event": "subscribe",
    #         "payload": ["1m", symbol.upper()]
    #     }) for symbol in symbols
    # ]
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
            "id": int(time.time()),
            "method": "kline.subscribe",
            "params": [symbol.upper(), 60]
        }) for symbol in symbols
    ]
    for sub in sub_data_list:
        print(sub)
        ws.send(sub)

    symbols_Events = []
    symbols_Data_List = {}
    while True:
        res = ws.recv()
        resJson = json.loads(res)
        # if isinstance(
        #         resJson, dict
        # ) and "event" in resJson and resJson["event"] == "subscribed":
        #     symbols_Events.append(resJson)
        # if isinstance(resJson, list):
        #     chanId = resJson[0]
        #     chanEvent = None
        #     for event in symbols_Events:
        #         if event["chanId"] == chanId:
        #             chanEvent = event
        #             break
        #     if chanEvent is not None:
        #         resJson[0] = chanEvent["key"]

        #     # ping pong
        #     if isinstance(resJson[1], str) and resJson[1] == "hb":
        #         pingStr = '{"event":"ping", "cid": ' + str(chanId) + '}'
        #         print(pingStr)
        #         ws.send(pingStr)

        #     if isinstance(resJson[1],
        #                   list) and len(resJson[1]) > 0 and isinstance(
        #                       resJson[1][0], list):
        #         continue
        #     elif isinstance(resJson[1], list) and len(resJson[1]) > 0:

        #         keySymbol = resJson[0]
        #         symbols_Data_List[keySymbol] = symbols_Data_List[
        #             keySymbol] + 1 if keySymbol in symbols_Data_List else 1
        #         print(len(symbols_Data_List), symbols_Data_List)

        print(resJson)
