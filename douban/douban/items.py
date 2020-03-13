# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    rate = scrapy.Field()
    img = scrapy.Field()
    director = scrapy.Field()
    category = scrapy.Field()
    language = scrapy.Field()
    release = scrapy.Field()
    runtime = scrapy.Field()
    votes = scrapy.Field()

