# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bmw.items import BmwItem


class Bmw7Spider(CrawlSpider):
    name = 'bmw7'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/153.html']

    rules = (
        Rule(LinkExtractor(allow=r'https://car.autohome.com.cn/pic/series/153.+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sort = response.xpath('//div[@class="uibox"]/div[@class="uibox-title"]/text()').extract_first()
        img_urls = response.xpath('//div[contains(@class,"uibox-con")]/ul/li//img/@src').extract()
        img_urls = list(map(lambda x: x.replace("240x180_0_q95_c42", "800x0_1_q95"), img_urls))
        img_urls = list(map(lambda x: response.urljoin(x), img_urls))
        item = BmwItem(sort=sort, image_urls=img_urls)
        print(img_urls)
        yield item

