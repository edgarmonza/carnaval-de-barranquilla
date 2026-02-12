import scrapy
from datetime import datetime, timezone

from scrapers.items import ArticleItem


class ElUniversalSpider(scrapy.Spider):
    """
    Scraper para noticias del Carnaval en El Universal de Cartagena.
    Cubre ampliamente el Carnaval de Barranquilla.
    """

    name = "eluniversal"
    allowed_domains = ["eluniversal.com.co"]
    start_urls = [
        "https://www.eluniversal.com.co/tags/carnaval-de-barranquilla",
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
    }

    def parse(self, response):
        """Parse the tag listing page for article links."""
        articles = response.css("article a::attr(href), .node-title a::attr(href), h2 a::attr(href)")

        for link in articles:
            url = link.get()
            if url:
                yield response.follow(url, callback=self.parse_article)

        # Follow pagination
        next_page = response.css("li.pager-next a::attr(href), a[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        """Parse an individual article page."""
        title = response.css("h1::text").get("").strip()

        if not title:
            return

        item = ArticleItem()
        item["title"] = title
        item["url"] = response.url
        item["source"] = "El Universal"

        item["author"] = response.css(
            "meta[name='author']::attr(content), .author::text"
        ).get("").strip()

        date_str = response.css(
            "time::attr(datetime), "
            "meta[property='article:published_time']::attr(content)"
        ).get("")
        item["published_at"] = date_str.strip() if date_str else None

        item["summary"] = response.css(
            "meta[property='og:description']::attr(content)"
        ).get("").strip()

        content_parts = response.css("article p::text, .article-body p::text").getall()
        item["content"] = "\n\n".join(p.strip() for p in content_parts if p.strip())

        item["image_url"] = response.css(
            "meta[property='og:image']::attr(content)"
        ).get("")

        item["category"] = "noticias"
        item["tags"] = response.css(".tags a::text").getall()
        item["scraped_at"] = datetime.now(timezone.utc).isoformat()

        yield item
