# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.htm
import re
from pymongo import MongoClient
# 建立数据库客户端，连接本地mongodb可省略ip和端口
client = MongoClient()
# 指定数据库和集合名字
collection = client['tencent']['hr']


class TencentPipeline(object):
    def process_item(self, item, spider):
        item['duty'] = self.process_duty(item['duty'])
        print(item)
        # 往数据库中插入数据
        collection.insert(item)
        return item

    def process_duty(self, duty):
        # 替换duty里的\r和\n,增强提取内容的可读性
        duty = re.sub(r'\r|\n', '', duty)
        return duty

