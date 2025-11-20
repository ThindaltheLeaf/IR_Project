from scraper.spiders.reddit_spider import RedditIkeaHacksSpider
from scraper.spiders.tosize_spider import TosizeSpider
from scraper.spiders.love_property_spider import LovePropertySpider
from scraper.spiders.ikea_spider import IkeaSpider
import os
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Make sure we can import "scraper.spiders"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = CURRENT_DIR  # this is the folder with scrapy.cfg
sys.path.append(PROJECT_ROOT)


if __name__ == "__main__":
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl(IkeaSpider)
    process.crawl(LovePropertySpider)
    process.crawl(TosizeSpider)
    process.crawl(RedditIkeaHacksSpider)

    process.start()
