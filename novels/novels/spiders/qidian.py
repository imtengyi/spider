# -*- coding: utf-8 -*-
import scrapy
import datetime
import time
import random
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from novels.items import NovelsItem
from novels.pipelines import NovelsPipeline


class QidianSpider(scrapy.Spider):
    name = "qidian"
    allowed_domains = ["a.qidian.com", "book.qidian.com"]
    start_urls = ['http://a.qidian.com/']
    mongo = NovelsPipeline()

    def parse(self, response):
        """
        Get the next pages and yield requests
        :param response:
        :return: request url
        """
        pages = response.css('div#page-container::attr(data-pagemax)').re(r'\d+')[0]
        for i in range(1, int(pages) + 1):
            time.sleep(random.randint(1, 5))
            url = self.start_urls[0] + "?page={i}".format(i=i)
            yield Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        """
        Get page URLs and yield Requests
        :param response:
        :return: request url
        """
        urls = response.css('.book-mid-info>h4>a::attr(href)').extract()
        for url in urls:
            url = "http:" + url
            is_exist = self.mongo.search_url(url)
            if not is_exist:
                time.sleep(random.randint(1, 3))
                print(url)
                yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        """
        This function parses a property page.
        :param response:
        :return: item
        """
        # Create the loader using response
        l = ItemLoader(item=NovelsItem(), response=response)
        # Load primary fields using css expressions
        l.add_css('name', '.book-info>h1>em::text', MapCompose(str.strip), TakeFirst())
        l.add_css('author', 'span>a.writer::text',
                  MapCompose(str.strip),
                  TakeFirst())
        l.add_css('cover', '#bookImg>img::attr(src)',
                  MapCompose(lambda s: "http:" + s, str.strip),
                  TakeFirst())
        l.add_css('novels_type', 'p.tag>a::text',
                  MapCompose(str.strip),
                  Join(separator='#'))
        l.add_css('status', 'p.tag>span.blue::text',
                  MapCompose(str.strip),
                  Join(separator='#'))
        l.add_css('abstract', 'div.book-intro>p::text',
                  MapCompose(str.strip),
                  Join())
        l.add_css('latest_chapter', 'p.cf>a.blue::text',
                  MapCompose(str.strip),
                  Join())

        # Housekeeping fields
        l.add_value('url', response.url)
        l.add_value('spider', self.name)
        l.add_value('date', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        yield l.load_item()
