# -*- coding: utf-8 -*-
import scrapy


class SpiderCsdnSpider(scrapy.Spider):
    name = 'spider_csdn'
    allowed_domains = ['csdn.net']
    start_urls = ['http://csdn.net/']

    def parse(self, response):
        print(response)
        print(response.url)
        print(response.body)
