# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem


class NovelsPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        _mongo_uri = 'mongodb://{account}{host}:{port}/{database}'.format(
            account='{username}:{password}@'.format(
                username=settings['MONGODB_USERNAME'],
                password=settings['MONGODB_PASSWORD']) if settings['MONGODB_USERNAME'] else '',
            host=settings['MONGODB_SERVER'] if settings['MONGODB_SERVER'] else 'localhost',
            port=settings['MONGODB_PORT'] if settings['MONGODB_PORT'] else 27017,
            database=settings['MONGODB_DB'])
        connection = pymongo.MongoClient(_mongo_uri)
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            data = {}
            for key, value in dict(item).items():
                data[key] = value[0] if value[0] else None
            self.collection.insert(data)
            return item

    def search_url(self, url):
        result = self.collection.find_one({'url': url})
        return True if result else False
