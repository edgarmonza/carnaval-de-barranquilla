import scrapy
from datetime import datetime, timezone

from scrapers.items import ArticleItem


class ElHeraldoSpider(scrapy.Spider):
    """
    Scraper para noticias del Carnaval de Barranquilla en El Heraldo.
    El Heraldo es el periódico principal de Barranquilla.
    """

    name = "elheraldo"
    allowed_domains = ["elheraldo.co"]
    start_urls = [
        "https://www.elheraldo.co/tags/carnaval-de-barranquilla",
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
    }

    def parse(self, response):
        """Parse the tag listing page for article links."""
        # Extract article links from the listing
        articles = response.css("article a::attr(href), .node-title a::attr(href), .views-row a::attr(href)")

        for link in articles:
            url = link.get()
            if url:
                yield response.follow(url, callback=self.parse_article)

        # Follow pagination
        next_page = response.css("li.pager-next a::attr(href), a.pager__link--next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        """Parse an individual article page."""
        title = (
            response.css("h1.node-title::text, h1.article-title::text, h1::text").get("").strip()
        )

        if not title:
            return

        # Extract article data
        item = ArticleItem()
        item["title"] = title
        item["url"] = response.url
        item["source"] = "El Heraldo"

        # Author
        item["author"] = (
            response.css(
                ".field-name-field-autor a::text, "
                ".author-name::text, "
                "span.byline::text, "
                "meta[name='author']::attr(content)"
            ).get("").strip()
        )

        # Published date
        date_str = response.css(
            "time::attr(datetime), "
            "meta[property='article:published_time']::attr(content), "
            "span.date::text"
        ).get("")
        item["published_at"] = date_str.strip() if date_str else None

        # Summary
        item["summary"] = (
            response.css(
                "meta[property='og:description']::attr(content), "
                "meta[name='description']::attr(content)"
            ).get("").strip()
        )

        # Content - try multiple selectors
        content_parts = response.css(
            ".field-name-body p::text, "
            ".article-body p::text, "
            ".node-content p::text, "
            "article p::text"
        ).getall()
        item["content"] = "\n\n".join(p.strip() for p in content_parts if p.strip())

        # Image
        item["image_url"] = response.css(
            "meta[property='og:image']::attr(content), "
            ".field-name-field-imagen img::attr(src), "
            "article img::attr(src)"
        ).get("")

        # Category
        item["category"] = "noticias"

        # Tags
        tags = response.css(
            ".field-name-field-tags a::text, "
            ".tags a::text"
        ).getall()
        item["tags"] = [t.strip() for t in tags if t.strip()]

        item["scraped_at"] = datetime.now(timezone.utc).isoformat()

        yield item
