# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class DoubanPipeline(object):
    def open_spider(self,spider):
        # 创建存储数据的文件
        self.file = open('douban.json','w')

    def process_item(self, item, spider):
        # 转换
        data = json.dumps(dict(item),ensure_ascii=False) + ',\n'
        # 写入
        self.file.write(data)

        return item

    def close_spider(self, spider):
        # 关闭存储数据的文件
        self.file.close()
