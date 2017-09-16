# -*- coding: utf-8 -*-
import scrapy
import time

from Tianqi.items import TianqiItem
# ----1 导入scrapy_redis爬虫类
from scrapy_redis.spiders import RedisSpider

# ----2 修改类的继承
class TianqiSpider(RedisSpider):
    name = 'tianqi'
    # ----3 注销允许的域以及起始的url

    # # 修改允许的域
    # allowed_domains = ['lishi.tianqi.com']
    # # 修改起始的url
    # start_urls = ['http://lishi.tianqi.com/']

    # ----4 动态获取允许的域名
    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(TianqiSpider, self).__init__(*args, **kwargs)
    # -----5 设置redis_key
    redis_key = 'tianqi:start_urls'

    # 解析起始的url对应的相应
    def parse(self, response):
        # 获取所有地区节点列表
        code_list = response.xpath('//*[@id="tool_site"]/div[2]/ul/li/a')
        # print(len(node_list))

        # 遍历节点列表
        print(len(code_list))
        for code in code_list[3:6]:
            area = code.xpath('./text()').extract_first()
            url = code.xpath('./@href').extract_first()
            # print(url, area)

            # 过滤错误url
            if url != '#':
                # 正确的url, 拿来发送请求
                yield scrapy.Request(url, callback=self.parse_area, meta={'meta_1':area})

    # 解析地区页面获取数据页面url 发起请求
    def parse_area(self, response):
        # 获取meta传参
        area = response.meta['meta_1']
        # 获取相信页面链接列表
        url_list = response.xpath('//*[@id="tool_site"]/div[2]/ul/li/a/@href').extract()
        # print(len(url_list))

        # 遍历url列表
        for url in url_list:
            # print(url,'-'*22)
            # 发起详细页面的请求
            yield scrapy.Request(url, callback=self.parse_data, meta={'meta_2':area})
            # print(url)
    # 解析详细页面
    def parse_data(self, response):
        # 获取meta传参
        area = response.meta['meta_2']
        # 获取url
        url = response.url
        # 获取采集时间
        timetamp = time.time()
        # 获取数据节点列表
        node_list = response.xpath('//*[@id="tool_site"]/div[@class="tqtongji2"]/ul')
        # print(len(node_list))

        # 遍历列表
        for node in node_list[1:4]:
            # 创建item对象 储存数据
            item = TianqiItem()

            # 抽取数据
            item['area'] = area
            item['timetamp'] = timetamp
            item['url'] = url
            # print('--'*20, item)

            try:
                item['datetime'] = node.xpath('./li[1]/a/text()').extract_first()
            except:
                item['max_t'] = node.xpath('./li[2]/text()').extract_first()

            # 最高气温
            item['min_t'] = node.xpath('./li[3]/text()').extract_first()
            # 天气
            item['weather'] = node.xpath('./li[4]/text()').extract_first()
            # 风向
            item['wind_direction'] = node.xpath('./li[5]/text()').extract_first()
            # 风力
            item['wind_power'] = node.xpath('./li[6]/text()').extract_first()

            # print(item)
            # 返回数据
            yield item


    #











