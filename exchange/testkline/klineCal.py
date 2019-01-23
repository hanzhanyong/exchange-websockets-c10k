import time
import requests
import pandas as pd


def log(func):
    def wrapper(*args, **kwargs):
        startTime = int(time.time() * 1000)
        # print(args)
        func(*args, **kwargs)
        endTime = int(time.time() * 1000)
        print("end-start: {}-{}={} ms".format(endTime, startTime,
                                              endTime - startTime))

    return wrapper


@log
def calKline(kline_df, kline_type_min):
    """
    kline_type_min: 3min 5min 15min 30min 60min 2h 4h 12h 1d 5d 7d 1m
    1min cal 3min 5min 15min 30min 60min 2h 4h 12h 1d 5d 7d 1m
    data
    """

    start = kline_df[0][0]
    while True:
        end = start + kline_type_min
        # search kline data from start to end values
        klineDf = kline_df[(kline_df['id'] > start) & (kline_df['id'] <= end)]

        print(klineDf)

        start = end

    # print(type(df))
    # 3min
    print(df[0:3], 3)


if __name__ == '__main__':
    huobipriUrl = "https://api.huobipro.com/market/history/kline?period=1min&size=2000&symbol=etcusdt&AccessKeyId=fff-xxx-ssss-kkk"
    r = requests.get(huobipriUrl, proxies={'https': '127.0.0.1:1087'})
    # print(r.json())
    df = pd.DataFrame(
        r.json()["data"],
        columns=['id', 'open', 'close', 'low', 'high', 'amount', 'vol'])
    calKline(df)
