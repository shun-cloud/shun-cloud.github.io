# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wechat.items import WechatItem


class SappSpider(CrawlSpider):
    name = 'sapp'
    allowed_domains = ['weixin.qq.com']
    start_urls = ['https://developers.weixin.qq.com/community/develop/question?page=1&tag=&type=0#post-list']

    rules = (
        Rule(LinkExtractor(allow=r'community/develop/question?page=\d+&tag=&type=0#post-list'), follow=True),
        Rule(LinkExtractor(allow=r'/community/develop/doc/.*'), callback='parse_item'),
    )

    def parse_item(self, response):
        # item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        title = response.xpath('//span[@class="post_title_content"]/text()').get()
        content = response.xpath('//div[@class="post_content"]//text()').getall()
        content = "".join(content).strip()
        item = WechatItem(title=title, content=content)
        print(item)
        return item
