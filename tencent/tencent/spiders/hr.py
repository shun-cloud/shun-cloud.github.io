# -*- coding: utf-8 -*-

import scrapy
import json
# import logging
from tencent.items import TencentItem
# logger = logging.getLogger(__name__)


class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['tencent.com']
    # 构建首页url地址
    url_1 = 'https://careers.tencent.com/tencentcareer/api/post/Query?pageIndex='
    page_index = 1
    url_2 = '&pageSize=10&language=zh-cn&area=cn'
    start_urls = [url_1 + str(page_index) + url_2]

    def parse(self, response):
        # 获取响应内容
        content = json.loads(response.body.decode())
        # 提取需要的数据
        data_list = content['Data']['Posts']
        for data in data_list:
            item = TencentItem()
            item['position'] = data["RecruitPostName"]
            item['city'] = data["LocationName"]
            item['duty'] = data["Responsibility"]
            item['update_time'] = data["LastUpdateTime"]
            yield item
        # 构建下一页url地址
        self.page_index += 1
        next_url = self.url_1 + str(self.page_index) + self.url_2
        # 指定处理下一页url的函数
        yield scrapy.Request(next_url, callback=self.parse)
