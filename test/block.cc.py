import requests
import time

# import json


def fech(url):
    rjson = None
    try:
        r = requests.get(url)
        rjson = r.json()
    except Exception as ex:
        print(url, ex)
    return rjson


'''
https://data.block.cc/api/v1

https://data.mifengcha.com/api/v2

'''


def getSymbols():
    url = "https://data.mifengcha.com/api/v2/symbols"
    rdata = fech(url)
    # for k in rdata:
    #     print(k)
    # symbolData = rdata["data"]
    symbolData = rdata
    symbolsMap = {symbol["symbol"]: symbol["name"] for symbol in symbolData}
    return symbolsMap


def main():

    symbolsMap = getSymbols()
    print(symbolsMap)
    url = "https://data.mifengcha.com/api/v2/price/history?symbol_name={}&start={}&end={}"
    # url = "https://data.mifengcha.com/api/v2/price?symbol="
    for k, v in symbolsMap.items():
        timestamp = int(time.time() * 1000)
        urlfech = url.format(v, timestamp - 60000, timestamp)
        print(urlfech)
        data = fech(urlfech)

        print(data)

    # for k, v in symbolsMap.items():
    #     c_url = url + v
    #     data = fech(c_url)
    #     print(data)


if __name__ == "__main__":
    main()
