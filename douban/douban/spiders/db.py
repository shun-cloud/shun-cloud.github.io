# -*- coding: utf-8 -*-
import scrapy
import json
import re
from douban.items import DoubanItem


class DbSpider(scrapy.Spider):
    name = 'db'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=1']
    num = 1

    def parse(self, response):
        content_list = json.loads(response.text)['subjects']
        try:
            for content in content_list:
                name = content["title"]
                rate = content["rate"]
                img = content['cover']
                url = content['url']
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_detail,
                    meta={"info": (name, rate, img)}
                )
        except Exception as e:
            print(e)
        else:
            if len(content_list) > 0:
                url_header = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start={}'
                self.num += 1
                next_url = url_header.format(self.num)
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                )

    def parse_detail(self, response):
        name, rate, img = response.meta.get("info")
        director = ",".join(response.xpath('//a[@rel="v:directedBy"]/text()').getall())
        category = "".join(response.xpath('//span[@property="v:genre"]//text()').getall())
        language = re.findall(r'<span class="pl">语言:</span>(.*?)<br/>', response.body.decode())[0].strip()
        release = "".join(response.xpath('//span[@property="v:initialReleaseDate"]/text()').getall())
        runtime = response.xpath('//span[@property="v:runtime"]/text()').get()
        votes = response.xpath('//span[@property="v:votes"]/text()').get()
        item = DoubanItem(
            name=name, rate=rate, img=img, director=director, category=category,
            language=language, release=release, runtime=runtime, votes=votes
        )
        print(item)
        yield item

