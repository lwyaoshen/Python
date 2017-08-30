# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re

from mzitu_scrapy.settings import IMAGES_STORE

headers = {
    'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Host':'i.meizitu.net',
    'Referer':'http://www.mzitu.com/101443/2',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'
}

class MzituScrapyPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        """
        :param request: 每一个图片下载管道请求
        :param response:
        :param info:
        :param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
        :return: 每套图的分类目录
        """
        item = request.meta['item']
        folder = item['name']
        folder_strip = strip(folder)
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
        return filename

    def get_media_requests(self, item, info):
        dic = IMAGES_STORE + item['name']
        #os.mkdir(dic)
        for img_url in item['image_urls']:
            yield Request(img_url, meta={'item': item},headers = headers)
            #urllib.request.urlretrieve(img_url, dic + '//' + img_url.split('/')[-1] + '.jpg');



    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    # def process_item(self, item, spider):
    #     return item

def strip(path):

    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path

