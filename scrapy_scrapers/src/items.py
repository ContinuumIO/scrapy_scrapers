import scrapy


class BodyItem(scrapy.Item):
    body = scrapy.Field()


class LinkItem(scrapy.Item):
    link = scrapy.Field()
    text = scrapy.Field()


class CustomItem(scrapy.Item):
    element = scrapy.Field()
