# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class IkeaHackItem(scrapy.Item):
    """Data structure for IKEA hack articles"""
    title = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    categories = scrapy.Field()
    tags = scrapy.Field()
    image_url = scrapy.Field()
    excerpt = scrapy.Field()