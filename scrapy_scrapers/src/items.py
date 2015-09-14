import scrapy


class LinkItem(scrapy.Item):
    link = scrapy.Field()
    text = scrapy.Field()
