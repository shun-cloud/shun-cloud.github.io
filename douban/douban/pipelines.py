# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors


class DoubanTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'mysql',
            'database': 'douban_movies',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None
    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into movies(id,name,rate,img,director,category,language,release_time,runtime,votes) values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(
            self.sql, (item['name'], item['rate'], item['img'], item['director'], item['category'], item['language'], item['release'], item['runtime'], item['votes'])
        )

    def handle_error(self, error, item, spider):
        print(error)
        print("-"*30 + "error" + "-"*30)

