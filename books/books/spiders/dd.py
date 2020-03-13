# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import scrapy
from copy import deepcopy
# import urllib
from urllib.parse import urljoin


class DdSpider(RedisSpider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://dangdang.com/']
    redis_key = "dd"

    def parse(self, response):
        div_list = response.xpath("//div[@class='con flq_body']/div")
        for div in div_list:
            item = {}
            item['top_kind'] = div.xpath("./dl/dt//text()").extract()
            item['top_kind'] = [i.strip() for i in item['top_kind'] if len(i.strip()) > 0]
            # item['top_kind'] = div.xpath("./dl/dt//text()").extract()
            dl_list = div.xpath(".//dl[@class='inner_dl']")
            for dl in dl_list:
                item['middle_kind'] = dl.xpath("./dt//text()").extract()
                item['middle_kind'] = item['middle_kind']
                item['middle_kind'] = [i.strip() for i in item['middle_kind'] if len(i.strip()) > 0][0]
                a_list = dl.xpath("./dd/a")
                for a in a_list:
                    item['bottom_href'] = a.xpath("./@href").extract_first()
                    item['bottom_kind'] = a.xpath("./@title").extract_first()
                    if item['bottom_href']:
                        yield scrapy.Request(
                            item['bottom_href'],
                            callback=self.parse_book_list,
                            meta={'item': deepcopy(item)}
                        )

    def parse_book_list(self, response):
        item = response.meta['item']
        li_list = response.xpath("//ul[@class='bigimg']/li")
        for li in li_list:
            item['book_name'] = li.xpath("./p[@class='name']/a/@title").extract_first()
            item['book_author'] = li.xpath("./p[@class='search_book_author']/span[1]//text()").extract_first()
            item['book_img'] = li.xpath("./a/img/@data-original").extract_first()
            item['book_price'] = li.xpath("./p[@class='price']/span/text()").extract_first()
            print(item)
        next_url = response.xpath("//a[@title='下一页']/@href").extract_first()
        if next_url:
            next_url = urljoin(response.url, next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item": item}
            )
