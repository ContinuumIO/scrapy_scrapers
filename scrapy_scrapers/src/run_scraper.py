import sys

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


allowed_domains = [sys.argv[1]]
start_urls = [x for x in sys.argv[2:]]


process = CrawlerProcess(get_project_settings())
process.crawl(
    "base",
    allowed_domains = allowed_domains,
    start_urls = start_urls,
)
process.start()
