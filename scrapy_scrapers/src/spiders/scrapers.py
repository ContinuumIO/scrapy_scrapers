import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


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
        item = {}
        item["body"] = response.body
        yield item

    def connect(self):
        self.process = CrawlerProcess(get_project_settings())

    def start(self):
        self.connect()
        self.process.crawl(
            self.name,
            start_urls = self.start_urls,
            allowed_domains = self.allowed_domains,
        )
        self.process.start()


class LinkScraper(BaseScraper):
    name = "links"

    def parse_as_item(self, response):
        for selector in response.xpath("//a"):
            item = {}
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
            item = {}
            item["element"] = selector.extract()
            yield item

    def start(self):
        self.connect()
        self.process.crawl(
            self.name,
            parser_string = self.parser_string,
            start_urls = self.start_urls,
            allowed_domains = self.allowed_domains,
        )
        self.process.start()
