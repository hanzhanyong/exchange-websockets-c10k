# -*- coding: utf-8 -*-
# author: hzy(306679711@qq.com)

from websocket import create_connection
import time

if __name__ == '__main__':
    cmdLine = "btcusdt@kline_5m"
    cmdLine = "btcusdt@depth5"
    wssUrl = "wss://stream.binance.com:9443/ws/" + cmdLine

    cmdLine2 = "ethusdt@depth5"

    wssUrl = "wss://stream.binance.com:9443/stream?streams=" + cmdLine  #+ "/" + cmdLine2
    while True:
        try:
            ws = create_connection(
                wssUrl, http_proxy_host="127.0.0.1", http_proxy_port=1087)
            break
        except Exception as ex:
            print('connect ws error,retry...{}'.format(ex))
            time.sleep(2)

    print('connect is started.')

    while True:
        res = ws.recv()
        print(res)
#         res=gzip.decompress(compressData).decode('utf-8')
#         ts = 0
#
#         if res[:7] == '{"ping"':
#             ts=res[8:21]
#             pong='{"pong":'+ts+'}'
#             ws.send(pong)
#             ws.send(tradeStr)
#         else:
#             result = json.loads(res)
#             if "ts" in result:
#                 ts = result["ts"]
