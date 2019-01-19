# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

from websocket import create_connection
# import gzip
import zlib
import time
import json


def inflate(data):
    decompress = zlib.decompressobj(-zlib.MAX_WBITS)  # see above
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated


if __name__ == '__main__':

    while True:
        try:
            ws = create_connection(
                "wss://real.okex.com:10441/websocket",
                http_proxy_host="127.0.0.1",
                http_proxy_port=1087)
            break
        except Exception as ex:
            print('connect ws error,retry...{}'.format(ex))
            time.sleep(2)

    print('connect is started.')

    # 订阅  Market Tickers 数据
    # tradeStr= "{'event':'addChannel','channel':'ok_sub_spot_bch_btc_ticker'}"
    tradeStr = "{'event':'addChannel','channel':'ok_sub_spot_bch_btc_ticker'}"
    # tradeStr= "{'event':'addChannel','channel':'all_ticker_3s'}"

    ws.send(tradeStr)
    while True:
        res = ws.recv()
        res = inflate(res)
        print(res)

        res = json.loads(res.decode("utf-8"))
        print(res)
        if type(res) is not list and res["event"] == "ping":
            res["event"] = "pong"
            print(res)
            ws.send(str(res))
