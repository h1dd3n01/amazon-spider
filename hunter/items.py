# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HunterItem(scrapy.Item):
    main_item = scrapy.Field()
    secondary_item = scrapy.Field()
