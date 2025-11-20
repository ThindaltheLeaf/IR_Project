# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.exceptions import NotConfigured


class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        mongo_uri = crawler.settings.get("MONGO_URI")
        mongo_db = crawler.settings.get("MONGO_DB_NAME")

        if not mongo_uri:
            raise NotConfigured("MONGO_URI is not set in settings or .env")

        return cls(mongo_uri=mongo_uri, mongo_db=mongo_db)

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Ensure source exists
        if not adapter.get("source"):
            adapter["source"] = spider.name

        # One collection per spider/website
        collection_name = f"hacks_{spider.name}"
        col = self.db[collection_name]

        # Upsert by URL to avoid duplicates
        col.update_one(
            {"url": adapter.get("url")},
            {"$set": adapter.asdict()},
            upsert=True,
        )
        return item
