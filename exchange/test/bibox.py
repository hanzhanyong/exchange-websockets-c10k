# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

from websocket import create_connection
import time
import json
import base64
import gzip

if __name__ == '__main__':
    while True:
        try:
            ws = create_connection(
                "wss://push.bibox.com/",
                http_proxy_host="127.0.0.1",
                http_proxy_port=1087)
            break
        except Exception as ex:
            print('connect ws error,retry...{}'.format(ex))
            time.sleep(2)

    print('connect is started.')

    # 订阅 KLine 数据
    # tradeStr = '{"event": "addChannel", "channel": "bibox_sub_spot_ETC_USDT_kline_1min"}'
    # ws.send(tradeStr)

    tradeStr = '{"event": "addChannel", "channel": "bibox_sub_spot_BTC_USDT_kline_1min"}'
    ws.send(tradeStr)
    while (True):
        msg = ws.recv()
        # print(msg)
        res = json.loads(msg)
        if "ping" in res:
            pong = msg.replace("ping", "pong")
            ws.send(pong)
            continue
        if not isinstance(res, list):
            continue
        if len(res) == 0 or "data" not in res[0]:
            continue
        res = res[0]
        data = res["data"]
        data = base64.b64decode(data)
        data = gzip.decompress(data).decode('utf-8')
        res["data"] = data
        print(res)
#
