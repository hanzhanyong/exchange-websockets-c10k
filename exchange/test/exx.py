# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

from websocket import create_connection
import gzip
import time

if __name__ == '__main__':
    while True:
        try:
            ws = create_connection(
                "wss://kline.exx.com/websocket",
                http_proxy_host="127.0.0.1",
                http_proxy_port=1087)
            break
        except Exception as ex:
            print('connect ws error,retry...{}'.format(ex))
            time.sleep(2)

    print('connect is started.')

    # 订阅  Market KLine 数据
    tradeStr = '{"dataType":"1_KLINE_30M_ETH_HSR","dataSize":1,"action":"ADD"}'
    tradeStr = '{event: "addChannel", channel: "ethusdt_cny_depth", isZip: false, binary: false}'

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
