import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class BaseScraper(CrawlSpider):
    name = "base"
    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item'),
    )

    def __init__(self, index, start_urls, allowed_domains=[], *args, **kwargs):
        self.allowed_domains = allowed_domains
        self.start_urls = start_urls
        self.index = index
        super(BaseScraper, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        item = {}
        item["body"] = response.body
        yield item

    # Instantiates a CrawlerProcess, which spins up a Twisted Reactor.
    def connect(self):
        self.process = CrawlerProcess(get_project_settings())

    # Start the scraper. The crawl process must be instantiated with the same
    # attributes as the instance.
    def start(self):
        self.connect()
        self.process.crawl(
            self.name,
            self.index,
            start_urls = self.start_urls,
            allowed_domains = self.allowed_domains,
        )
        self.process.start()


class LinkScraper(BaseScraper):
    name = "links"

    def parse_item(self, response):
        for selector in response.xpath("//a"):
            item = {}
            item["link"] = selector.xpath("@href").extract()
            item["text"] = selector.xpath("text()").extract()
            yield item


class CustomScraper(BaseScraper):
    """
    Scraper for custom parser arguemnts. Currently only accepts xpath parser
    arguments.
    """
    name = "custom"

    def __init__(self, parser_string, parser_dict, *args, **kwargs):
        self.parser_string = parser_string
        self.parser_dict = parser_dict
        super(CustomScraper, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        for selector in response.xpath(self.parser_string):
            item = {}
            for key in self.parser_dict.keys():
                item[key] = selector.xpath(self.parser_dict[key]).extract()
            yield item

    def start(self):
        self.connect()
        self.process.crawl(
            self.name,
            index=self.index,
            parser_string=self.parser_string,
            parser_dict=self.parser_dict,
            start_urls=self.start_urls,
            allowed_domains=self.allowed_domains,
        )
        self.process.start()
