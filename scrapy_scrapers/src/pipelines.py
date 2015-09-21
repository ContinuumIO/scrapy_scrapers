import json

from elasticsearch import Elasticsearch


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open("crawl.json", "wb")

    def process_item(self, item, spider):
        line = json.dumps(dict(item))
        self.file.write(line)
        return item


class ElasticsearchPipeline(object):
    batch_size = 500

    def __init__(self):
        self.es = Elasticsearch()
        self.batch = []

    def open_spider(self, spider):
        pass

    def add_to_index(self, data):
        pass

    def process_item(self, item, spider):
        self.batch.append(item)
        if len(self.batch) == self.batch_size:
            print(self.batch)

    def close_spider(self, spider):
        pass
