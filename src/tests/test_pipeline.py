import unittest
import time

from elasticsearch import Elasticsearch
from pipelines import ElasticsearchPipeline
from spiders.scrapers import CustomScraper



class TestElasticsearchPipeline(unittest.TestCase):

    def setUp(self):
        self.es = Elasticsearch()
        self.pipeline = ElasticsearchPipeline()
        self.spider = CustomScraper(
            index="test_index",
            start_urls=["http://www.dmoz.org"],
            parser_string="//a",
            parser_dict={
                "text": "text()",
                "link": "@href",
            }
        )
        self.pipeline.open_spider(self.spider)

    def tearDown(self):
        self.es.indices.delete(self.spider.index)

    def get_index_content(self):
        return self.es.search(self.spider.index, doc_type=self.spider.name)

    def get_index_length(self):
        return self.get_index_content()["hits"]["total"]

    # Wait until the number of documents in the index is stable, then allow for
    # assertions.
    def index_creation_wait(self):
        initial_length = self.get_index_length()
        time.sleep(1)
        while initial_length != self.get_index_length():
            time.sleep(1)
            initial_length = self.get_index_length()

    def test_process_item(self):
        item = {"link": ["http://www.continuum.io/"]}
        for x in range(1000):
            self.pipeline.process_item(item, self.spider)
        self.index_creation_wait()
        assert self.get_index_length() == 1000
        assert not self.pipeline.batch
        # Delete the previous index and start over with a new pipeline.
        self.pipeline.open_spider(self.spider)
        self.pipeline.process_item(item, self.spider)
        self.pipeline.close_spider(self.spider)
        self.index_creation_wait()
        assert self.get_index_length() == 1
