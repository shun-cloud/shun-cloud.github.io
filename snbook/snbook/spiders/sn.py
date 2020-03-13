# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re

class SnSpider(scrapy.Spider):
    name = 'sn'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/book.html']

    def parse(self, response):
        # 顶层类
        div_list = response.xpath("//div[@class='menu-item']")
        # 中间类
        div_sub_list = response.xpath("//div[contains(@class,'menu-sub')]")
        for div in div_list:
            item = {}
            # 顶层分类的名字
            item['top_kind'] = div.xpath(".//h3/a/text()").extract_first()
            # 中间分类的位置
            sub_div = div_sub_list[div_list.index(div)]
            p_list = sub_div.xpath(".//p")
            for p in p_list:
                item['middle_kind'] = p.xpath("./a/text()").extract_first()
                li_list = sub_div.xpath(".//ul/li")
                for li in li_list:
                    item['bottom_kind'] = li.xpath("./a/text()").extract_first()
                    item['bottom_href'] = li.xpath("./a/@href").extract_first()
                    print(item['bottom_href'])
                    yield scrapy.Request(
                        item['bottom_href'],
                        callback=self.parse_book_list,
                        meta={"item": deepcopy(item)}
                    )

    def parse_book_list(self, response):
        item = response.meta['item']
        li_list = response.xpath("//ul[@class='clearfix']/li")
        for li in li_list:
            item['book_title'] = li.xpath(".//div[@class='res-info']//a[@class='sellPoint']/text()").extract_first()
            item['book_href'] = li.xpath(".//div[@class='res-info']//a[@class='sellPoint']/@href").extract_first()
            item['book_href'] = "http:" + item['book_href']
            # print(item['book_title'])
            yield scrapy.Request(
                item['book_href'],
                callback=self.parse_book_detail,
                meta={"item": deepcopy(item)}
            )
        # next_url = response.xpath(".//a[@id='nextPage']/@href").extract_first()
        # print(next_url)
        url = "http://list.suning.com/emall/showProductList.do?ci={}&pg=03&cp={}&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAABC&id=IDENTIFYING&cc=376"
        ci = item['bottom_href'].split('-')[1]
        current_page = re.findall('param.currentPage = "(.*?)";', response.body.decode())[0]
        page_numbers = re.findall('param.pageNumbers = "(.*?)";', response.body.decode())[0]
        if int(current_page) < (int(page_numbers) - 1):
            next_page = int(current_page) + 1
            next_url = url.format(ci, next_page)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item": item}
            )

    def parse_book_detail(self, response):
        item = response.meta['item']
        # print(response.body.decode())
        item['book_img'] = response.xpath(".//a[@id='bigImg']/img/@src").extract_first()
        item['book_img'] = "http:" + item['book_img']
        # item['book_price'] = response.xpath(".//span[@class='mainprice']/text()").extract_first()
        item['book_price'] = re.findall(r'"itemPrice":(.*?),', response.body.decode())
        item['book_price'] = item['book_price'][0] if len(item['book_price']) > 0 else None
        yield item
