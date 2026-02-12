import hashlib


class DeduplicationPipeline:
    """Detecta y elimina items duplicados basándose en URL."""

    def __init__(self):
        self.seen_urls = set()

    def process_item(self, item, spider):
        url = item.get("url", "")
        url_hash = hashlib.md5(url.encode()).hexdigest()

        if url_hash in self.seen_urls:
            spider.logger.info(f"Duplicate found: {url}")
            from scrapy.exceptions import DropItem
            raise DropItem(f"Duplicate item: {url}")

        self.seen_urls.add(url_hash)
        return item
