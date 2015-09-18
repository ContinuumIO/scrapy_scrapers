import scrapy

from items import BodyItem


class PageScraper(scrapy.Spider):
    name = "page"

    def __init__(self, allowed_domains=[], start_urls=[], *args, **kwargs):
        self.allowed_domains = allowed_domains
        self.start_urls = start_urls
        super(PageScraper, self).__init__(*args, **kwargs)

    def parse(self, response):
        for href in response.xpath("//a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_as_item)

    def parse_as_item(self, response):
        item = BodyItem()
        item["body"] = response.body
        yield item
