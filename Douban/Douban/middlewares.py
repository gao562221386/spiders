# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from Douban.settings import USER_AGNET_LIST
from Douban.settings import PROXY_LIST
import base64

# from scrapy.conf import settings
import random

class DoubanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class RandomUserAgentMilleware(object):

    def process_request(self, request, spider):
        # 获取上一个随机的用户头
        ua = random.choice(USER_AGNET_LIST)
        # print (ua)
        # 设置用户头参数
        request.headers['User-Agent'] = ua



class RandomIPProxyMiddleware(object):
    def process_request(self,request,spider):
        # 随机获取一个ip代理
        proxy = random.choice(PROXY_LIST)
        # print (proxy)
        # 判断是否有账号密码
        # if proxy.has_key('user_passwd'):
        if 'user_passwd' in proxy:
            # 对账号密码进行编码
            b64_user_pwd = base64.b64encode(proxy['user_passwd'].encode())
            # 设置账号密码
            request.headers['Proxy-Authorization'] = 'Basic ' + b64_user_pwd.decode()
            # 使用代理
            request.meta['proxy'] = 'http://' + proxy['ip_port']
        else:
            # 免费代理
            request.meta['proxy'] = 'http://' + proxy['ip_port']
