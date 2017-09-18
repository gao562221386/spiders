# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Zhiyouji.items import ZhiyoujiItem
import time

# ----1 导入类
from  scrapy_redis.spiders import RedisCrawlSpider

# ----2 修改类的继承
# class ZhiyoujiSpider(CrawlSpider):
class ZhiyoujiSpider(RedisCrawlSpider):
    name = 'zhiyouji'

    # ----3 注销允许的域和起始url列表
    # # 修改允许的域名
    # allowed_domains = ['www.jobui.com']
    # # 修改起始url列表
    # start_urls = ['http://www.jobui.com/cmp']

    # ----4 动态获取允许的域
    def __init__(self,*args,**kwargs):
        domain = kwargs.pop('domain','')
        self.allowed_domains = list(filter(None,domain.split(',')))
        super(ZhiyoujiSpider,self).__init__(*args,**kwargs)

    # ----5 设定redis_key
    redis_key = 'zhiyouji:start_urls'

    rules = (
        # 提取列表页面url,因为不需要提取数据，所以将callback删除
        Rule(LinkExtractor(allow=r'/cmp\?n=\d+#listInter'), follow=True),
        # 提取企业详情url,follow决定是否在响应中继续应用链接提取器
        Rule(LinkExtractor(allow=r'/company/\d+/$'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        # print ('------',response.url)

        # 创建item对象实例
        item = ZhiyoujiItem()

        # 抽取数据
        item['url'] = response.url
        item['timestamp'] = time.time()

        # 企业名
        item['company'] = response.xpath('//*[@id="companyH1"]/a/text()').extract_first()
        # 浏览次数
        item['views'] = response.xpath('//div[@class="grade cfix sbox"]/div[1]/text()').extract_first().split('人')[0].strip()
        #
        item['slogan'] = response.xpath('/html/body/div[3]/div[1]/div/div[1]/div[2]/p/text()').extract_first()
        # 企业性质
        try:
            item['category'] = response.xpath('//*[@id="cmp-intro"]/div/div[2]/dl/dd[1]/text()').extract_first().split('/')[0].strip()
        except:
            item['category'] = response.xpath('//*[@id="cmp-intro"]/div/div/dl/dd[1]/text()').extract_first()
        # 企业规模
        try:
            item['number'] = response.xpath('//*[@id="cmp-intro"]/div/div[2]/dl/dd[1]/text()').extract_first().split('/')[-1]
        except:
            item['number'] = response.xpath('//*[@id="cmp-intro"]/div/div/dl/dd[1]/text()').extract_first()
        # 行业
        item['industry'] = response.xpath('//dd[@class="comInd"]/a/text()').extract()
        # 简称
        item['short_name'] = response.xpath('//*[@id="cmp-intro"]/div/div[2]/dl/dd[3]/text()').extract_first()
        # 简介
        item['desc'] = ''.join(response.xpath('//*[@id="textShowMore"]/text()').extract())

        # 好评度
        item['praise'] = response.xpath('//div[@class="swf-contA"]/div/h3/text()').extract_first()
        # 薪资范围
        item['salary_range'] = response.xpath('//div[@class="swf-contB"]/div/h3/text()').extract_first()
        # 企业产品
        item['products'] = response.xpath('/html/body/div[4]/div[1]/div[1]/div[4]/div/div/div/a/text()').extract()
        # 融资信息
        data_list = []
        node_list = response.xpath('//div[@class="jk-matter jk-box fs16"]/ul/li')
        for node in node_list:
            data = {}
            data['datetime'] = node.xpath('./span[1]/text()').extract_first()
            data['status'] = node.xpath('./h3/text()').extract_first()
            data['sum'] = node.xpath('./span[2]/text()').extract_first()
            data['investors'] = node.xpath('./span[3]/text()').extract_first()
            data_list.append(data)
        item['finance_info'] = data_list

        # 获取排名信息
        data_list = []
        node_list = response.xpath('//div[@class="fs18 honor-box"]/div')
        # print (len(node_list))
        for node in node_list:
            data = {}
            key = node.xpath('./a/text()').extract_first()
            value = node.xpath('./span[2]/text()').extract_first()
            data[key] = value
            data_list.append(data)
        item['rank_info'] = data_list

        # 获取地址
        item['address'] = response.xpath('//dl[@class="dlli fs16"]/dd[1]/text()').extract_first()
        # 公司网址
        item['website'] = response.xpath('//dl[@class="dlli fs16"]/dd[2]/a/text()').extract_first()
        # 联系方式
        item['contact'] = response.xpath('//div[@class="j-shower1 dn"]/dd/text()').extract_first()
        # qq
        item['qq'] = response.xpath('//span[@class="contact-qq"]/text()').extract_first()

        # 返回数据
        yield item