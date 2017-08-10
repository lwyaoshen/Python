from scrapy import Spider,Request
from scrapy.selector import HtmlXPathSelector


class gif_spider(Spider):
    name = 'gif';
    start_urls = ["http://tu.duowan.com/m/bxgif"];

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename,'wb') as f:
            f.write(response.body);





