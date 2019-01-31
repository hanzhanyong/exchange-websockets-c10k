# exchange-websockets-c10k
test websockets of exchange(i.e    huobipro  binance  okex),     asyncio and aiohttp

data: ticker + kline(1min) + depth + trade

framework: multithread + websockets + asyncio + redis + rabbitmq

author: 
    hzy(306679711@qq.com)


## Scrapy Install & Test
--pip3 install scrapy
--pip3 install scrapy-splash
cd <dir>
scrapy startproject <scrapyTestProject>
scrapy genspider spider_baidu image.baidu.com
scrapy crawl spider_baidu --nolog

setting: ROBOTSTXT_OBEY = False (spider baidu.com)






