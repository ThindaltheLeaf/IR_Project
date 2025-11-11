import scrapy
from ikea_hacks_scraper.items import IkeaHackItem
from datetime import datetime

class IkeaSpider(scrapy.Spider):
    name = 'ikea'
    allowed_domains = ['ikeahackers.net']
    
    start_urls = [
        'https://ikeahackers.net/category/hacks',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1,  # Be polite - 1 second between requests
    }
    
    def parse(self, response):
        """
        Parse the category listing page
        Extract individual hack article links
        """
        # Get all article links from the page
        article_links = response.css('article.post h2.entry-title a::attr(href)').getall()
        
        self.logger.info(f'Found {len(article_links)} articles on page: {response.url}')
        
        # Follow each article link
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)
        
        # Find and follow the "next page" link
        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page:
            self.logger.info(f'Following next page: {next_page}')
            yield response.follow(next_page, callback=self.parse)
    
    def parse_article(self, response):
        """
        Parse individual IKEA hack article page
        Extract all relevant data
        """
        item = IkeaHackItem()
        
        # Extract title
        item['title'] = response.css('h1.entry-title::text').get()
        
        # Extract content (all paragraphs in the article body)
        content_paragraphs = response.css('div.entry-content p::text').getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])
        
        # Extract author
        item['author'] = response.css('span.author a::text').get()
        
        # Extract date
        date_str = response.css('time.entry-date::attr(datetime)').get()
        item['date'] = date_str
        
        # Extract URL
        item['url'] = response.url
        
        # Extract categories
        item['categories'] = response.css('span.cat-links a::text').getall()
        
        # Extract tags
        item['tags'] = response.css('span.tag-links a::text').getall()
        
        # Extract featured image
        item['image_url'] = response.css('div.entry-content img::attr(src)').get()
        
        # Extract excerpt/description
        excerpt = response.css('div.entry-content p::text').get()
        item['excerpt'] = excerpt[:200] + '...' if excerpt and len(excerpt) > 200 else excerpt
        
        self.logger.info(f'Scraped article: {item["title"]}')
        
        yield item