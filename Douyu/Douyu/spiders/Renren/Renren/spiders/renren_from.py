# -*- coding: utf-8 -*-
import scrapy


class RenrenFromSpider(scrapy.Spider):
    name = 'renren_from'
    allowed_domains = ['www.renren.com']
    start_urls = ['http://www.renren.com/']

    def parse(self, response):
        # 构建登录数据
        form_data = {
            "email": "17173805860",
            "password": "1qaz@WSX3edc"
        }
        yield scrapy.FormRequest.from_response(response,formdata=form_data,callback=self.parse_login)

    def parse_login(self, response):
        with open('renren2.html','w')as f:
            f.write(response.text)