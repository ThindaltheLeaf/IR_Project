# IKEA Hacks Crawler

Scrapy-based web crawlers for collecting IKEA hack projects from multiple sources.

## Features

- **Multi-source Scraping**: ikeahackers.net, loveproperty.com, tosize.it, r/ikeahacks
- **MongoDB Storage** with automatic deduplication
- **Configurable crawl limits** and delays
- **Respectful crawling** with robots.txt compliance

## Setup

### Prerequisites

- Python 3.9+
- MongoDB Atlas account



### Installation

```bash
cd crawler
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
````

### Environment Variables

Create a `.env` file in crawler:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=ikea_hacks_ir 
```

## Running Crawlers

### Run All Crawlers

```bash
python scraper/run_crawlers.py
```

### Run Individual Spiders

```bash
cd scraper

# IKEA Hackers
scrapy crawl ikea

# Love Property
scrapy crawl loveproperty

# Tosize
scrapy crawl tosize

# Reddit
scrapy crawl reddit
```

## Spiders

### 1. IKEA Spider (`ikea`)

Crawls [ikeahackers.net](https://ikeahackers.net)

- **Collection**: `hacks_ikea`
- **Features**: Article listing, pagination, category extraction
- **Yield**: ~6000+ hacks

### 2. Love Property Spider (`loveproperty`)

Crawls [loveproperty.com](https://loveproperty.com)

- **Collection**: `hacks_loveproperty`
- **Features**: Gallery/slideshow parsing, junk filtering
- **Yield**: ~100+ hacks

### 3. Tosize Spider (`tosize`)

Crawls [tosize.it](https://tosize.it)

- **Collection**: `hacks_tosize`
- **Features**: Project listing, pagination
- **Yield**: ~200+ hacks

### 4. Reddit Spider (`reddit`)

Crawls [r/ikeahacks](https://reddit.com/r/ikeahacks)

- **Collection**: `hacks_reddit`
- **Features**: JSON API, pagination, post metadata
- **Limit**: 2000 posts
- **Note**: Ignores robots.txt (with custom User-Agent)

## Data Model

Each hack document contains:

```python
{
    "source": str,           # Spider name
    "title": str,
    "content": str,          # Full text
    "author": str,
    "date": str,             # ISO format
    "url": str,
    "categories": [str],
    "tags": [str],
    "image_url": str,
    "excerpt": str           # Short description
}
```

## Building Combined Collection

After crawling, merge all collections into `hacks_all`:

```bash
python scraper/build_hacks_all.py
```

This script:

1. Drops existing `hacks_all` collection
2. Merges all `hacks_*` collections
3. Deduplicates by (url, source)
4. Ensures consistent source field

## Configuration

### Settings (`settings.py`)

```python
# Concurrency
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

# Respect robots.txt (except reddit spider)
ROBOTSTXT_OBEY = True

# MongoDB pipeline
ITEM_PIPELINES = {
    "scraper.pipelines.MongoPipeline": 300,
}
```

### Spider-specific Settings

Each spider can override settings:

```python
custom_settings = {
    "DOWNLOAD_DELAY": 2.0,
    "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
}
```


## Troubleshooting

### Rate Limiting

If you encounter rate limiting, increase `DOWNLOAD_DELAY`:

```python
DOWNLOAD_DELAY = 3.0
```

### MongoDB Connection

Verify your connection string:

```bash
python -c "from pymongo import MongoClient; print(MongoClient('your-uri').server_info())"
```

### Robot Exclusion

Some sites may block scrapers. The Reddit spider bypasses this with:

```python
custom_settings = {
    "ROBOTSTXT_OBEY": False,
}
```

## Project Structure

```
crawler/
├── scraper/
│   ├── scraper/
│   │   ├── spiders/
│   │   │   ├── ikea_spider.py
│   │   │   ├── love_property_spider.py
│   │   │   ├── tosize_spider.py
│   │   │   └── reddit_spider.py
│   │   ├── items.py           # Data models
│   │   ├── pipelines.py       # MongoDB pipeline
│   │   └── settings.py        # Scrapy config
│   ├── run_crawlers.py        # Run all spiders
│   ├── build_hacks_all.py     # Merge collections
│   └── scrapy.cfg
├── requirements.txt
└── .env
```

## Data Quality

The crawlers include:

- Junk content filtering
- Duplicate detection
- URL normalization
- Image URL fixing (Reddit relative URLs)

