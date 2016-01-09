import os
import subprocess
import unittest
import SimpleHTTPServer
import SocketServer

import requests
from elasticsearch import Elasticsearch
from scrapy.http import Request, TextResponse

from spiders.scrapers import CustomScraper


class TestCustomScraper(unittest.TestCase):

    def setUp(self):
        self.body = open(os.path.join(os.path.dirname(__file__),
            "test_pages/dmoz_index.html"), "r").read()
        self.url = "http://www.example.com/"
        self.request = Request(self.url)
        self.response = TextResponse(self.url, request=self.request, body=self.body, encoding='utf-8')
        self.scraper = CustomScraper(
            index="test_index",
            start_urls=[self.url],
            parser_string="//a",
            parser_dict={
                "text": "text()",
                "link": "@href",
            }
        )

    def test_parse(self):
        parsed = list(self.scraper.parse_item(self.response))
        assert parsed[1] == {'text': [u'about dmoz'], 'link': [u'http://www.dmoz.org/docs/en/about.html']}
