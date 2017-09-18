# -*- coding: utf-8 -*-
import scrapy


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['www.renren.com']
    start_urls = ['http://www.renren.com/PLogin.do']

    def start_requests(self):
        # 构建登录数据
        form_data = {
            "email": "17173805860",
            "password": "1qaz@WSX3edc"
        }

        # 发送post请求,start_requests发起的请求默认由parse方法解析
        yield scrapy.FormRequest(self.start_urls[0],formdata=form_data)

    def parse(self, response):
        with open('renren.html','wb')as f:
            f.write(response.body)