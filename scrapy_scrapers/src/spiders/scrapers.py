import scrapy

from items import LinkItem


class BaseScraper(scrapy.Spider):
    name = "base"

    def __init__(self, allowed_domains=[], start_urls=[], *args, **kwargs):
        self.allowed_domains = allowed_domains
        self.start_urls = start_urls
        super(BaseScraper, self).__init__(*args, **kwargs)

    def parse(self, response):
        for href in response.xpath("//a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_as_item)

    def parse_as_item(self, response):
        for selector in response.xpath("//a"):
            item = LinkItem()
            item["link"] = selector.xpath("@href").extract()
            item["text"] = selector.xpath("text()").extract()
            yield item
