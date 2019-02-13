# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

from websocket import create_connection
import gzip
import time

if __name__ == '__main__':
    while True:
        try:
            ws = create_connection(
                "wss://www.bitmex.com/realtime",
                http_proxy_host="127.0.0.1",
                http_proxy_port=1087)
            break
        except Exception as ex:
            print('connect ws error,retry...{}'.format(ex))
            time.sleep(2)

    print('connect is started.')

    tradeStr = '{"op": "subscribe", "args": ["trade:XBTUSD","instrument:XBTUSD"]}'
    ws.send(tradeStr)
    while (True):
        compressData = ws.recv()
        print(compressData)
        # res = gzip.decompress(compressData).decode('utf-8')

        # print(res)

        # if res[:7] == '{"ping"':
        #     ts = res[8:21]
        #     pong = '{"pong":' + ts + '}'
        #     ws.send(pong)
#
