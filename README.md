# exchange-websockets-c10k
    test websockets of exchange(i.e    huobipro  binance  okex)
    subscribe data: ticker + kline(1min) + depth + trade

# author
    email: 306679711@qq.com
    weixi: h13426492793

# technology stack
    threading
    websockets
    asyncio
    aiohttp
    aioredis 
    aiorabbitmq




## Scrapy Install & Test
--pip3 install scrapy
--pip3 install scrapy-splash
cd <dir>
scrapy startproject <scrapyTestProject>
scrapy genspider spider_baidu image.baidu.com

cd scrapyTest/scrapyTest
scrapy crawl spider_baidu --nolog


setting: ROBOTSTXT_OBEY = False (spider baidu.com)






