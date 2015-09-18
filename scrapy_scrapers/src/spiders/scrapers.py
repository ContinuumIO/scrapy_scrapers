import scrapy

from items import BodyItem, LinkItem, CustomItem


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
        item = BodyItem()
        item["body"] = response.body
        yield item


class LinkScraper(BaseScraper):
    name = "links"

    def parse_as_item(self, response):
        for selector in response.xpath("//a"):
            item = LinkItem()
            item["link"] = selector.xpath("@href").extract()
            item["text"] = selector.xpath("text()").extract()
            yield item


class CustomScraper(BaseScraper):
    name = "custom"

    def __init__(self, parser_string, *args, **kwargs):
        self.parser_string = parser_string
        super(CustomScraper, self).__init__(*args, **kwargs)

    def parse_as_item(self, response):
        for selector in response.xpath(self.parser_string):
            item = CustomItem()
            item["element"] = selector.extract()
            yield item
