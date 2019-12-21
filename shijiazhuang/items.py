# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShijiazhuangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #新闻标题
    news_title = scrapy.Field()
    #新闻日期
    news_time = scrapy.Field()
    #新闻来源
    news_source = scrapy.Field()
    #新闻内容
    news_content = scrapy.Field()

