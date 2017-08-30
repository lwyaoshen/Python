from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from mzitu_scrapy.items import MzituScrapyItem


class mzitu_spider(CrawlSpider):
    name = 'mzitu'
    allowed_domains = ['mzitu.com']
    start_urls = ['http://www.mzitu.com/']
    #start_urls = ['http://www.mzitu.com/92107']
    image_urls = []
    rules = (
        Rule(LinkExtractor(allow=('http://www.mzitu.com/\d{1,6}',), deny=('http://www.mzitu.com/\d{1,6}/\d{1,6}')),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print('正在处理' + response.url)
        dic_name = response.xpath('//div[@class="content"]/h2/text()').extract_first()
        #print('---------------------------------------------------------------------------------------------',dic_name)
        max_num = response.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()').extract_first()
        #print(dic_name)
        #print(max_num)
        item = MzituScrapyItem();
        item['name'] = dic_name
        for detail in range(1,int(max_num)+1):
            page_url = response.url + '/' + str(max_num)
            #print('+++++++++++++++++++++++++++' + str(detail),page_url)
            yield Request(page_url, callback=self.img_url)
        item['image_urls'] = self.image_urls
        yield item

    def img_url(self, response):
        img_urls = response.xpath("descendant::div[@class='main-image']/descendant::img/@src").extract()
        for img_url in img_urls:
            self.image_urls.append(img_url)
        #print('*********************',self.image_urls)
