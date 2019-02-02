# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BaiduimagesItem(scrapy.Item):
    thumbURL = scrapy.Field()
    # replaceUrl = scrapy.Field()
    # adType = scrapy.Field()
    # middleURL = scrapy.Field()
    # largeTnImageUrl = scrapy.Field()
    # hasLarge = scrapy.Field()
    # hoverURL = scrapy.Field()
    # pageNum = scrapy.Field()
    objURL = scrapy.Field()
    fromURL = scrapy.Field()
    # fromURLHost = scrapy.Field()
    # currentIndex = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    imgType = scrapy.Field()
    # isGif = scrapy.Field()
    # filesize = scrapy.Field()
    # bdSrcType = scrapy.Field()
    # bdImgnewsDate = scrapy.Field()
    title = scrapy.Field()
    # bdSourceName = scrapy.Field()
    # bdFromPageTitlePrefix = scrapy.Field()
    # token = scrapy.Field()
    # imgCs = scrapy.Field()
    # imgOs = scrapy.Field()
    # base64 = scrapy.Field()
    pass
