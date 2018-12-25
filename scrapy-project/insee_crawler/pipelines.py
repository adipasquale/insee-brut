# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from insee_crawler.mongo_provider import MongoProvider


class MongoPipeline(object):

    def __init__(self, settings):
        self.mongo_provider = MongoProvider(
            settings.get('MONGO_URI'),
            settings.get('MONGO_DATABASE')
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        self.collection = self.mongo_provider.get_collection()

    def close_spider(self, spider):
        self.mongo_provider.close_connection()

    def process_item(self, item, spider):
        item["_scrapy_item_class"] = item.__class__.__name__
        self.collection.find_one_and_update(
            {"id_insee": item["id_insee"]},
            {"$set": dict(item)},
            upsert=True
        )
        return item
