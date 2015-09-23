import unittest

from pipelines import ElasticsearchPipeline


class TestElasticsearchPipeline(unittest.TestCase):

    def setUp(self):
        self.pipeline = ElasticsearchPipeline()
        self.scraper = CustomScraper(
            index="test_index",
            start_urls=[self.url],
            parser_string="//a",
            parser_dict={
                "text": "text()",
                "link": "@href",
            }
        )

    def test_nothing(self):
        assert 1
