import unittest
from elasticsearch import Elasticsearch


class ElasticsearchTest(unittest.TestCase):

    def setUp(self):
        self.es = Elasticsearch()

    def test_elasticsearch_up(self):
        assert self.es.ping()

    def test_create_index(self):
        index = self.es.indices.create(index="test_index")
        assert index == {u'acknowledged': True}

    def test_delete_index(self):
        index = self.es.indices.delete(index="test_index")
        assert index == {u'acknowledged': True}
