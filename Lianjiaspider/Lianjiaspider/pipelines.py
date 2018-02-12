# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from pymongo import MongoClient

class LianjiaspiderPipeline(object):
    def __init__(self):
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        dbname = settings['MONGO_DBNAME']
        colname = settings['MONGO_COLNAME']

        #创建数据库链接
        self.client = MongoClient(host,port)
        #选择数据库
        self.db = self.client[dbname]
        #选择集合
        self.col = self.db[colname]


    def process_item(self, item, spider):
        #将item类的实例转换成字典
        dict_data = dict(item)
        #插入数据
        self.col.insert(dict_data)
        return item

    def __del__(self):
        self.client.close()