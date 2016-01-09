import json

from elasticsearch import Elasticsearch, helpers


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open("crawl.json", "wb")

    def process_item(self, item, spider):
        line = json.dumps(dict(item))
        self.file.write(line)
        return item


class ElasticsearchPipeline(object):
    batch_size = 1000

    def open_spider(self, spider):
        self.es_instance = Elasticsearch()
        self.batch = []
        self.index = spider.index
        if self.es_instance.indices.exists(index=self.index):
            self.es_instance.indices.delete(self.index)
        self.es_instance.indices.create(self.index)

    def process_item(self, item, spider):
        self.batch.append({"_source": item, "_type": spider.name})
        if len(self.batch) >= self.batch_size:
            helpers.bulk(client=self.es_instance, actions=self.batch, index=self.index)
            self.batch = []

    def close_spider(self, spider):
        if self.batch:
            helpers.bulk(client=self.es_instance, actions=self.batch, index=self.index)
