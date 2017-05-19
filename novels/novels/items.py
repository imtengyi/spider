# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class NovelsItem(Item):
    # Primary fields
    name = Field()
    author = Field()
    cover = Field()
    novels_type = Field()
    status = Field()
    abstract = Field()
    latest_chapter = Field()

    # Housekeeping fields
    url = Field()
    spider = Field()
    date = Field()
