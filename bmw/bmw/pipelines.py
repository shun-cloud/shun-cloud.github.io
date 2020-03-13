# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import os
from bmw import settings


class BmwPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        request_objs = super(BmwPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(BmwPipeline, self).file_path(request, response, info)
        sort = request.item.get('sort')
        images_store = settings.IMAGES_STORE
        sort_path = os.path.join(images_store, sort)
        if not os.path.exists(sort_path):
            os.mkdir(sort_path)
        image_name = path.replace("full/", "")
        image_path = os.path.join(sort_path, image_name)
        return image_path


