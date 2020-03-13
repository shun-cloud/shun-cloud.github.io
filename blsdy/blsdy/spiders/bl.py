# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import json


class BlSpider(CrawlSpider):
    name = 'bl'
    allowed_domains = ['80s.tw']
    start_urls = ['http://www.80s.tw/movie/list']

    rules = (
        Rule(LinkExtractor(allow=r'/movie/\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/movie/list/-----p/d+'), follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        item['name'] = re.findall(r'var title="(.*?)";', response.body.decode())
        item['pub_time'] = response.xpath('//div[@class="info"]/div[1]/span[5]//text()').extract()
        # item['link'] = response.xpath('//span[@class="label_pianyuan"]//a[@rel="nofollow"]/@href').extract_first()
        # item['link'] = re.findall(r'<a rel="nofollw" href="(.*?)" thunderrestitle', response.body.decode())[0]
        # item['link'] = re.findall(r'type="checkbox" value="(.*?)" checked="checked"', response.body.decode())[0]
        item['link'] = re.findall(r'thunderHref="(.*?)" thunderPid', response.body.decode())[0]
        print(item)
        item = json.dumps(item, ensure_ascii=False)
        # content_list = []
        # content_list = content_list.append(item)
        # print(type(item))
        with open("movie.txt", "a", encoding="utf-8") as f:
            # for content in content_list:
            #     f.write(content)
            f.write(item)
            f.write("\n")
        return None

