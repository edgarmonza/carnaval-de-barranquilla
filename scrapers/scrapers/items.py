import scrapy


class ArticleItem(scrapy.Item):
    """Noticias y artículos sobre el Carnaval."""
    title = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    author = scrapy.Field()
    published_at = scrapy.Field()
    summary = scrapy.Field()
    content = scrapy.Field()
    image_url = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    scraped_at = scrapy.Field()


class EventItem(scrapy.Item):
    """Eventos del Carnaval: desfiles, fiestas, comparsas."""
    title = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    description = scrapy.Field()
    event_date = scrapy.Field()
    event_time = scrapy.Field()
    location = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    image_url = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    scraped_at = scrapy.Field()


class BusinessItem(scrapy.Item):
    """Negocios y servicios: hoteles, restaurantes, transporte."""
    name = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    rating = scrapy.Field()
    review_count = scrapy.Field()
    image_url = scrapy.Field()
    opening_hours = scrapy.Field()
    price_range = scrapy.Field()
    scraped_at = scrapy.Field()


class ProductItem(scrapy.Item):
    """Productos: merchandising, artesanías, disfraces."""
    name = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    image_url = scrapy.Field()
    category = scrapy.Field()
    seller = scrapy.Field()
    availability = scrapy.Field()
    scraped_at = scrapy.Field()


class PlanItem(scrapy.Item):
    """Planes turísticos y paquetes."""
    title = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    duration = scrapy.Field()
    includes = scrapy.Field()
    image_url = scrapy.Field()
    provider = scrapy.Field()
    category = scrapy.Field()
    scraped_at = scrapy.Field()
