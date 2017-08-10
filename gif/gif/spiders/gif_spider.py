from scrapy import Spider

class gif_spider(Spider):
    name = 'gif';
    allowd_domains = ['duowan.com']
    start_urls = ["http://tu.duowan.com/m/bxgif/"]

    def parse(self, response):
        filename = response.url.split("/")[-2];
        with open(filename,'wb') as f:
            f.write(response.body);
