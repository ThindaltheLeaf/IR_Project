import scrapy
from ikea_hacks_scraper.items import IkeaHackItem

class TosizeSpider(scrapy.Spider):
    name = 'tosize'
    allowed_domains = ['tosize.it']
    
    start_urls = [
        'https://www.tosize.it/en-it/diy/type/ikea-hacks',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }
    
    def parse(self, response):
        """
        Parse the listing page - extract project links
        """
        # we get all links
        project_links = response.css('article.project a.project-link::attr(href)').getall()
        
        if not project_links:
            project_links = response.css('div.project-item a::attr(href)').getall()
        
        self.logger.info(f'Found {len(project_links)} projects on page: {response.url}')
        
        for link in project_links:
            # Full URLs needed for this spider
            full_url = response.urljoin(link)
            yield scrapy.Request(full_url, callback=self.parse_project)
        
        next_page = response.css('a.next::attr(href)').get()
        if not next_page:
            next_page = response.css('link[rel="next"]::attr(href)').get()
        
        if next_page:
            self.logger.info(f'Following next page: {next_page}')
            yield response.follow(next_page, callback=self.parse)
    
    def parse_project(self, response):
        """
        Parse individual project page
        """
        item = IkeaHackItem()
        
        # Title extraction
        item['title'] = response.css('h1::text').get()
        if not item['title']:
            item['title'] = response.css('title::text').get()
        
        # Content extraction
        content_parts = response.css('div.project-description p::text').getall()
        if not content_parts:
            content_parts = response.css('div.content p::text').getall()
        item['content'] = ' '.join([p.strip() for p in content_parts if p.strip()])
        
        # Author extraction
        item['author'] = response.css('span.author::text').get()
        if not item['author']:
            item['author'] = response.css('div.author-name::text').get()
        if not item['author']:
            item['author'] = 'Tosize Community'
        
        # date extraction
        item['date'] = response.css('time::attr(datetime)').get()
        if not item['date']:
            item['date'] = response.css('span.date::text').get()
        
        # URL
        item['url'] = response.url
        
        # Categories and tags
        item['categories'] = response.css('span.category a::text').getall()
        item['tags'] = response.css('span.tag::text').getall()
        if not item['tags']:
            item['tags'] = ['ikea-hacks', 'diy']
        
        # images
        item['image_url'] = response.css('div.project-image img::attr(src)').get()
        if not item['image_url']:
            item['image_url'] = response.css('img.main-image::attr(src)').get()
        
        # Excertpt
        if item['content']:
            excerpt = item['content'][:200] + '...' if len(item['content']) > 200 else item['content']
            item['excerpt'] = excerpt
        else:
            item['excerpt'] = item['title']
        
        self.logger.info(f'Scraped project: {item["title"]}')
        
        yield item