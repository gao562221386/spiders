# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ZhiyoujiItem(scrapy.Item):
    # define the fields for your item here like:
    # 采集url
    url = scrapy.Field()
    # 采集时间
    timestamp = scrapy.Field()
    # 企业名
    company = scrapy.Field()
    # 浏览次数
    views = scrapy.Field()
    # 口号
    slogan = scrapy.Field()
    # 企业性质
    category = scrapy.Field()
    # 企业规模
    number = scrapy.Field()
    # 行业
    industry = scrapy.Field()
    # 企业简称
    short_name = scrapy.Field()
    # 企业简介
    desc = scrapy.Field()
    # 好评读
    praise = scrapy.Field()
    # 薪资范围
    salary_range = scrapy.Field()
    # 产品
    products = scrapy.Field()
    # 融资情况
    finance_info = scrapy.Field()
    # 排名信息
    rank_info = scrapy.Field()
    # 公司地址
    address = scrapy.Field()
    # 企业网站
    website = scrapy.Field()
    # 联系方式
    contact = scrapy.Field()
    # qq
    qq = scrapy.Field()

