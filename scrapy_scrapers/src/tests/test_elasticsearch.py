import unittest
from elasticsearch import Elasticsearch


class ElasticsearchTest(unittest.TestCase):

    def setUp(self):
        self.es = Elasticsearch()

    def tearDown(self):
        pass

    def test_elasticsearch_up(self):
        self.assertTrue(self.es.ping())

    def test_create_index(self):
        index = self.es.indices.create(index="potato")
        self.assertEqual(index, {u'acknowledged': True})

    def test_delete_index(self):
        index = self.es.indices.delete(index="potato")
        self.assertEqual(index, {u'acknowledged': True})


if __name__ == '__main__':
    unittest.main()
