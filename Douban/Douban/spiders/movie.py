# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Douban.items import DoubanItem

class MovieSpider(CrawlSpider):
    name = 'movie'
    # 修改允许的域名
    allowed_domains = ['movie.douban.com']
    # 修改起始的url列表
    start_urls = ['https://movie.douban.com/top250']

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+&filter='), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # print (response.url,'----------')
        # 获取所有电影节点
        node_list = response.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]')
        # print (len(node_list))

        # 遍历节点列表
        for node in node_list:
            # 创建item对象
            item = DoubanItem()
            # 从节点中获取数据，保存到item中
            # 电影名
            item['name'] = node.xpath('./div[1]/a/span[1]/text()').extract_first()
            # 评分
            item['score'] = node.xpath('./div[2]/div/span[2]/text()').extract_first()
            # info信息
            item['info'] = ''.join([i.strip() for i in node.xpath('./div[2]/p[1]/text()').extract()]).replace('\xa0','')
            #简介
            item['desc'] = node.xpath('./div[2]/p[2]/span/text()').extract_first()

            # print (item)
            # 返回数据
            yield item