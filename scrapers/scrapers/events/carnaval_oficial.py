import scrapy
from datetime import datetime, timezone

from scrapers.items import EventItem


class CarnavalOficialSpider(scrapy.Spider):
    """
    Scraper para la página oficial del Carnaval de Barranquilla.
    Fuente primaria de eventos, programación y contenido oficial.
    """

    name = "carnaval_oficial"
    allowed_domains = ["carnavaldebarranquilla.org"]
    start_urls = [
        "https://www.carnavaldebarranquilla.org",
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
    }

    def parse(self, response):
        """Parse the main page and follow links to events/programming."""
        # Look for links to events, programming, schedule
        event_links = response.css(
            "a[href*='programacion']::attr(href), "
            "a[href*='evento']::attr(href), "
            "a[href*='agenda']::attr(href), "
            "a[href*='calendario']::attr(href)"
        ).getall()

        for link in event_links:
            yield response.follow(link, callback=self.parse_event_listing)

        # Also follow any content links
        content_links = response.css(
            "a[href*='noticia']::attr(href), "
            "a[href*='historia']::attr(href)"
        ).getall()

        for link in content_links:
            yield response.follow(link, callback=self.parse_content)

    def parse_event_listing(self, response):
        """Parse a listing page of events."""
        events = response.css("article, .event-item, .evento")

        for event in events:
            link = event.css("a::attr(href)").get()
            if link:
                yield response.follow(link, callback=self.parse_event)

        # Also try to extract events directly from the listing
        if not events:
            # Try parsing the current page as a single event
            yield from self.parse_event(response)

    def parse_event(self, response):
        """Parse an individual event page."""
        title = response.css("h1::text, h2.event-title::text").get("").strip()

        if not title:
            return

        item = EventItem()
        item["title"] = title
        item["url"] = response.url
        item["source"] = "Carnaval de Barranquilla (Oficial)"

        item["description"] = response.css(
            "meta[property='og:description']::attr(content), "
            ".event-description::text, "
            ".description p::text"
        ).get("").strip()

        # Try to extract date/time
        date_text = response.css(
            ".event-date::text, .fecha::text, time::attr(datetime)"
        ).get("")
        item["event_date"] = date_text.strip() if date_text else None

        time_text = response.css(".event-time::text, .hora::text").get("")
        item["event_time"] = time_text.strip() if time_text else None

        item["location"] = response.css(
            ".event-location::text, .lugar::text, .ubicacion::text"
        ).get("").strip()

        item["address"] = response.css(
            ".event-address::text, .direccion::text"
        ).get("").strip()

        item["image_url"] = response.css(
            "meta[property='og:image']::attr(content)"
        ).get("")

        item["category"] = "eventos"

        price_text = response.css(".event-price::text, .precio::text").get("")
        if price_text:
            item["price"] = price_text.strip()

        item["scraped_at"] = datetime.now(timezone.utc).isoformat()

        yield item

    def parse_content(self, response):
        """Parse content/informational pages from the official site."""
        from scrapers.items import ArticleItem

        title = response.css("h1::text").get("").strip()
        if not title:
            return

        item = ArticleItem()
        item["title"] = title
        item["url"] = response.url
        item["source"] = "Carnaval de Barranquilla (Oficial)"
        item["summary"] = response.css(
            "meta[property='og:description']::attr(content)"
        ).get("").strip()

        content_parts = response.css("article p::text, .content p::text").getall()
        item["content"] = "\n\n".join(p.strip() for p in content_parts if p.strip())

        item["image_url"] = response.css(
            "meta[property='og:image']::attr(content)"
        ).get("")
        item["category"] = "cultura"
        item["tags"] = ["carnaval", "oficial"]
        item["scraped_at"] = datetime.now(timezone.utc).isoformat()

        yield item
