# -*- coding: utf-8 -*-
import scrapy
import json
from Douyu.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    # 修改允许的域
    allowed_domains = ['capi.douyucdn.cn']
    host = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=100&offset='
    offset = 0
    # 修改起始url
    start_urls = [host]

    def parse(self, response):
        # print (response.body)
        # 将源码转换成python字典
        data_list = json.loads(response.body)['data']

        # 遍历数据列表
        for data in data_list:
            # 创建item对象
            item = DouyuItem()
            # 提取数据，将data中对应的字段提取出来，保存到item中
            item['name'] = data['nickname']
            item['uid'] = data['owner_uid']
            item['image_link'] = data['vertical_src']
            item['city'] = data['anchor_city']
            # print (item)
            # 反回数据
            yield item

        #翻页
        if len(data_list) != 0:
            self.offset += 100
            # 生成出url
            next_url = self.host + str(self.offset)
            # 创建请求并发送
            yield scrapy.Request(next_url,callback=self.parse)

