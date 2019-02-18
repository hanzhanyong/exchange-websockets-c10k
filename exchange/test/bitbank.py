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
    tradeStr = '42["join-room", "candlestick_btc_jpy"]'
    # tradeStr = '42["join-room", "ticker_btc_jpy"]'
    ws.send(tradeStr)
    ping = "2"
    timeStamp = time.time()
    timeStampStart = timeStamp
    try:
        while (True):
            res = ws.recv()
            print(type(res), res)
            # print(res[0:2] == "40")
            # if res[0:2] == "40":
            #     print(res[0:2] == "40")
            #     ws.send(tradeStr)

            timeStampEnd = time.time()
            # print("timeStampEnd - timeStamp", timeStampEnd - timeStamp)
            if timeStampEnd - timeStamp > 30:
                timeStamp = timeStampEnd
                print("ping", ping)
                ws.send(ping)
    except Exception as ex:
        print(ex)
    print("end-start=", timeStampEnd - timeStampStart)
