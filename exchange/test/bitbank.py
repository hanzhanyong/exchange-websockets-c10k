# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

from websocket import create_connection
import time

if __name__ == '__main__':
    while True:
        try:
            ws = create_connection(
                "wss://stream.bitbank.cc/socket.io/?EIO=3&transport=websocket",
                http_proxy_host="127.0.0.1",
                http_proxy_port=1087)
            break
        except Exception as ex:
            print('connect ws error,retry...{}'.format(ex))
            time.sleep(2)

    print('connect is started.')

    # 订阅 KLine 数据
    tradeStr = '42["join-room", "candlestick_eth_btc"]'

    while (True):
        res = ws.recv()
        print(type(res), res)
        # print(res[0:2] == "40")
        if res[0:2] == "40":
            print(res[0:2] == "40")
            ws.send(tradeStr)

        # ws.send('2')
        # res = gzip.decompress(compressData).decode('utf-8')

        # print(res)

        # if res[:7] == '{"ping"':
        #     ts = res[8:21]
        #     pong = '{"pong":' + ts + '}'
        #     ws.send(pong)
#
