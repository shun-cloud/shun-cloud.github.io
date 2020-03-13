# -*- coding: utf-8 -*-
import scrapy
import json
import demjson
import re
from copy import deepcopy

class JjSpider(scrapy.Spider):
    name = 'jj'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://fund.eastmoney.com/data/rankhandler.aspx?op=dy&dt=kf&ft=hh&rs=&gs=0&sc=qjzf&st=desc&sd=2019-11-01&ed=2020-02-21&es=0&qdii=&pi=1&pn=50']

    def parse(self, response):
        content = response.body.decode()
        data_list = re.findall(r'{datas:(.*?),allRecords', content)[0]
        data_list = eval(data_list)
        # print(type(data_list))
        # print(type(data_list))
        # num = 1
        for data in data_list:
            item = {}
            # item['排名'] = num
            item['编号'] = data.split(",")[0]
            item['名字'] = data.split(",")[1]
            item['涨幅'] = data.split(",")[3]
            item['涨幅'] = item['涨幅'] + "%"
            item['起始日期'] = data.split(",")[6]
            print(item)
            # num += 1
            item = json.dumps(item, ensure_ascii=False)
            with open("基金.txt", "a", encoding="utf-8") as f:
                # for content in content_list:
                #     f.write(content)
                f.write(item)
                f.write("\n")
            page_index = re.findall(r'pageIndex:(.*?),', content)[0]
            all_pages = re.findall(r'allPages:(.*?),', content)[0]
            if int(page_index) < int(all_pages):
                next_page = int(page_index) + 1
                url ='http://fund.eastmoney.com/data/rankhandler.aspx?op=dy&dt=kf&ft=hh&rs=&gs=0&sc=qjzf&st=desc&sd=2019-11-01&ed=2020-02-21&es=0&qdii=&pi={}&pn=50'
                next_url = url.format(next_page)
                yield scrapy.Request(
                    next_url,
                    callback=self.parse,
                    meta={"item": deepcopy(item)}
                )
                yield item

