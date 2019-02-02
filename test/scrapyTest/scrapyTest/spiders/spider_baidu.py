# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware
from scrapy.http import Request, HtmlResponse
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

from ..items import BaiduimagesItem


class SpiderBaiduSpider(scrapy.Spider):
    name = 'spider_baidu'
    allowed_domains = ['baidu.com']
    start_urls = [
        'http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=%E7%89%A1%E4%B8%B9%E8%8A%B1'
    ]

    # request需要封装成SplashRequest
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                self.parse,
                args={'wait': '0.5'}
                # ,endpoint='render.json'
            )

    def parse(self, response):
        site = Selector(response)
        it_list = []

        images = site.xpath('//li[@class="imgitem"]').extract()
        for imgStr in images:

            # print(type(imgStr))
            imgSel = Selector(text=imgStr)
            # print(imgStr)
            # dataValues = imgSel.xpath('//li/@data-objurl').extract()
            # # print(type(dataValues), dataValues)
            # dataUrl = ""
            # for v in dataValues:
            #     dataUrl += str(v)
            # print(dataUrl)
            thumbURL = imgSel.xpath('//li/@data-thumburl').extract()[0]
            objURL = imgSel.xpath('//li/@data-objurl').extract()[0]
            fromURL = imgSel.xpath('//li/@data-fromurl').extract()[0]
            width = imgSel.xpath('//li/@data-width').extract()[0]
            height = imgSel.xpath('//li/@data-height').extract()[0]
            imgType = imgSel.xpath('//li/@data-ext').extract()[0]
            title = imgSel.xpath('//li/@data-title').extract()[0]

            item = BaiduimagesItem(
                thumbURL=thumbURL,
                objURL=objURL,
                fromURL=fromURL,
                width=width,
                height=height,
                imgType=imgType,
                title=title)
            it_list.append(item)
            print(item)
            """
            <li class="imgitem" style="width: 253px; height: 200px; margin-right: 0px; margin-bottom: 5px;" data-objurl="http://pic.51yuansu.com/pic3/cover/00/87/14/58daf385f0b03_610.jpg" data-thumburl="http://img0.imgtn.bdimg.com/it/u=1786517352,3618013954&amp;fm=26&amp;gp=0.jpg" data-fromurl="ippr_z2C$qAzdH3FAzdH3Fooo_z&amp;e3Bc8y7wgf7_z&amp;e3Bv54AzdH3FfvAzdH3F6fqvtzgyir_z&amp;e3Bip4s" data-fromurlhost="www.51yuansu.com" data-ext="jpg" data-saved="0" data-pi="0" data-specialtype="0" data-cs="1786517352,3618013954" data-width="610" data-height="488" data-hostname="" data-title="&lt;strong&gt;牡丹花&lt;/strong&gt;" data-personalized="0" data-partnerid="0">
            """
            # print(type(img), img)
        # it['price'] = prices[0].extract() + prices[1].extract()
        # print '京东价：' + it['price']

        # print(type(response.body))
        # body = response.body.decode("UTF-8")
        # print(len(body))
        # print(body[40133:79133])
        # imgList = response.xpath('//li[@class="imgitem"]')
        # print(imgList[0])

        # images = json.loads(response.body)
        # print(images)
        # for image in images:
        #     item = BaiduimagesItem()
        #     try:
        #         item['url'] = image.get('thumbURL')
        #         yield item
        #     except Exception as e:
        #         print(e)
        pass
