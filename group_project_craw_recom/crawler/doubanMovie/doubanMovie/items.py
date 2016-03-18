# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanmovieItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    # title = scrapy.Field()
    # url = scrapy.Field()
    # rate = scrapy.Field()
    # movieid = scrapy.Field()
    cover = scrapy.Field()
    year = scrapy.Field()
    score = scrapy.Field()
    director = scrapy.Field()
    classification = scrapy.Field()
    actor = scrapy.Field()
    url = scrapy.Field()
    movieid = scrapy.Field()
    pass
