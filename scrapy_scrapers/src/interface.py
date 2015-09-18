import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class CrawlerInterface(object):

    def __init__(self, crawler, start_urls, allowed_domains=[]):
        self.crawler = crawler
        self.start_urls = start_urls
        self.allowed_domains = allowed_domains
        self.process = CrawlerProcess(get_project_settings())

    def start(self):
        self.process.crawl(
            self.crawler,
            allowed_domains=self.allowed_domains,
            start_urls=self.start_urls
        )
        self.process.start()
