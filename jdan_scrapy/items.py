# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdanScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field()
    support_votes = scrapy.Field()
    unsupport_votes = scrapy.Field()
    comments_count = scrapy.Field()
    #pics = scrapy.Field()
    image_urls = scrapy.Field()
