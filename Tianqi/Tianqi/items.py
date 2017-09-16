# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TianqiItem(scrapy.Item):
    # define the fields for your item here like:
    # 采集url
    url = scrapy.Field()
    # 城市
    area = scrapy.Field()
    # 采集日期
    timetamp = scrapy.Field()
    # 最高气温
    max_t = scrapy.Field()
    # 最低气温
    min_t = scrapy.Field()
    # 天气
    weather = scrapy.Field()
    # 风向
    wind_direction = scrapy.Field()
    # 风力
    wind_power = scrapy.Field()

    datetime =scrapy.Field()
    pass
