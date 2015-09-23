# Scraper

This project is designed to handle the broad issues involved in scraping the web for content. It uses scrapy, and may in the future integrate other scrapers like BeautifulSoup and grab.

To begin scraping, create an instance of one of the scraper classes. Currently there is only a BodyScraper, a LinkScraper, and a CustomScraper. Only the CustomScraper requires you to supply the `parser_string` and `parser_dict` arguments.

Here is some example code, to be run from the `scrapy_scrapers/src` directory.
```
import scrapy

from spiders.scrapers import CustomScraper


spider = CustomScraper(
    index="reddit",
    start_urls=[
        "http://www.reddit.com/"
    ],
    parser_string="//div[contains(@class,'entry unvoted')]/p[contains(@class,'title')]",
    parser_dict={
        "title": "a/text()",
        "link": "a/@href",
    },
)
spider.start()
```
This scraper will go through reddit and grab all of the titles and links to content. Currently the custom scraper requires a parser_string as a starting point and a parser_dict containing items to be scraped.

The scrapers currently only support parsers using Scrapy's xpath tools, but there are plans for including other parsers in the future. Currently, to properly use this tool a user will have to be familiar with xpath parsing.

Requirements:
- The scraper requires a running elasticsearch instance, running at port 9200. The scraper will automatically populate elasticsearch. The environment.yml file will install elasticsearch and kibana, which you can start by running `elasticsearch` and `kibana` in separate terminal sessions.
