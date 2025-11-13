import scrapy
from ikea_hacks_scraper.items import IkeaHackItem
import json
import re

class RedditSpider(scrapy.Spider):
    name = 'reddit'
    allowed_domains = ['reddit.com']
    
    start_urls = [
        'https://www.reddit.com/r/ikeahacks.json',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  
        'USER_AGENT': 'IkeaHacksScraper/1.0 (Educational IR Project)',
    }
    
    page_count = 0
    max_pages = 20 
    
    def parse(self, response):
        """
        Parse Reddit JSON response
        """
        try:
            data = json.loads(response.text)
            posts = data['data']['children']
            
            self.logger.info(f'Found {len(posts)} posts on page {self.page_count + 1}')
            
            for post in posts:
                post_data = post['data']
                
                if post_data.get('stickied'):
                    continue
                
                item = IkeaHackItem()
                
                # Title extraction
                item['title'] = post_data.get('title', '')
                
                # Content extraction
                selftext = post_data.get('selftext', '')
                item['content'] = selftext if selftext else post_data.get('url', '')
                
                # Authorextraction
                item['author'] = post_data.get('author', 'unknown')
                
                # Date extraction
                created_utc = post_data.get('created_utc')
                if created_utc:
                    from datetime import datetime
                    item['date'] = datetime.fromtimestamp(created_utc).isoformat()
                
                # URL
                item['url'] = f"https://www.reddit.com{post_data.get('permalink', '')}"
                
                # Categories extraction
                item['categories'] = ['r/ikeahacks']
                flair = post_data.get('link_flair_text')
                if flair:
                    item['categories'].append(flair)
                
                # Tags extraction
                item['tags'] = self.extract_tags(item['title'] + ' ' + str(item['content']))
                
                # Image extraction
                thumbnail = post_data.get('thumbnail')
                if thumbnail and thumbnail.startswith('http'):
                    item['image_url'] = thumbnail
                else:
                    item['image_url'] = post_data.get('url') if post_data.get('url', '').endswith(('.jpg', '.png', '.gif')) else None
                
                # Excerpt extraction
                if selftext:
                    item['excerpt'] = selftext[:200] + '...' if len(selftext) > 200 else selftext
                else:
                    item['excerpt'] = item['title']
                
                self.logger.info(f'Scraped Reddit post: {item["title"][:50]}...')
                
                yield item
            
            # Pagination
            after = data['data'].get('after')
            self.page_count += 1
            
            if after and self.page_count < self.max_pages:
                next_url = f'https://www.reddit.com/r/ikeahacks.json?after={after}'
                self.logger.info(f'Following next page: {self.page_count + 1}')
                yield scrapy.Request(next_url, callback=self.parse)
        
        except json.JSONDecodeError as e:
            self.logger.error(f'Failed to parse JSON: {e}')
        except KeyError as e:
            self.logger.error(f'Missing expected key in Reddit data: {e}')
    
    def extract_tags(self, text):
        """
        Extract common IKEA-related keywords as tags
        """
        text_lower = text.lower()
        common_ikea_items = ['kallax', 'billy', 'lack', 'hemnes', 'malm', 'pax', 'eket', 
                            'ivar', 'besta', 'stuva', 'alex', 'nordli', 'brimnes']
        
        tags = ['ikea', 'hack', 'diy']
        
        for item in common_ikea_items:
            if item in text_lower:
                tags.append(item)
        
        return list(set(tags))[:5]