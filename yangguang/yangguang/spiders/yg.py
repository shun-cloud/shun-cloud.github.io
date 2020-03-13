# -*- coding: utf-8 -*-
import scrapy
from yangguang.items import YangguangItem


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    '''
    url = 'http://wz.sun0769.com/index.php/question/report?page='
    page = 0
    start_urls = [url + str(page)]
    '''
    start_urls = ['http://wz.sun0769.com/index.php/question/report?page=0']

    def parse(self, response):
        tr_list = response.xpath("//div[@class='newsHead clearfix']/table[2]/tr")
        for tr in tr_list:
            item = YangguangItem()
            item['title'] = tr.xpath("./td[3]/a[1]/@title").extract_first()
            item['href'] = tr.xpath('./td[3]/a[1]/@href').extract_first()
            item['update_time'] = tr.xpath('./td[last()]/text()').extract_first()
            yield scrapy.Request(
                item['href'],
                callback=self.parse_detail,  # 指定处理详情页的函数
                meta={"item": item}
            )
        # 构建下一页url地址
        next_url = response.xpath("//a[text()='>']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self, response):  # 处理详情页
        item = response.meta['item']
        item['img'] = response.xpath("//td[@class='txt16_3']//img/@src").extract()
        #  完善img的地址
        item['img'] = ['http://wz.sun0769.com' + i for i in item['img']]
        item['text'] = response.xpath("//td[@class='txt16_3']//text()").extract_first()
        yield item
