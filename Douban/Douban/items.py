# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # 电影名
    name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 电影信息
    info = scrapy.Field()
    # 电影的简介
    desc = scrapy.Field()
    pass
