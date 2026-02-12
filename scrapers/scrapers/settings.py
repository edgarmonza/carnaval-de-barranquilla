BOT_NAME = "carnaval_scrapers"

SPIDER_MODULES = ["scrapers.news", "scrapers.social", "scrapers.business", "scrapers.events", "scrapers.products"]
NEWSPIDER_MODULE = "scrapers.news"

# Respectful scraping
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 1.5
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# User agent
USER_AGENT = "CarnavalDeBarranquilla Bot (+https://github.com/edgarmonza/carnaval-de-barranquilla)"

# Pipeline
ITEM_PIPELINES = {
    "scrapers.pipeline.cleaning.CleaningPipeline": 100,
    "scrapers.pipeline.dedup.DeduplicationPipeline": 200,
    "scrapers.pipeline.storage.SupabasePipeline": 300,
}

# Feeds - local backup
FEEDS = {
    "output/%(name)s_%(time)s.jsonl": {
        "format": "jsonlines",
        "encoding": "utf-8",
    },
}

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"

# AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Cache (for development)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400  # 24 hours
HTTPCACHE_DIR = ".scrapy_cache"
