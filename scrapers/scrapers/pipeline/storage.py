import os
import logging

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class SupabasePipeline:
    """Almacena items en Supabase (PostgreSQL)."""

    def __init__(self):
        self.client = None

    def open_spider(self, spider):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if url and key:
            try:
                from supabase import create_client
                self.client = create_client(url, key)
                spider.logger.info("Connected to Supabase")
            except Exception as e:
                spider.logger.warning(f"Could not connect to Supabase: {e}")
                spider.logger.info("Items will only be saved to local files")
        else:
            spider.logger.info("Supabase not configured. Items will only be saved to local files")

    def process_item(self, item, spider):
        if not self.client:
            return item

        table = self._get_table_name(item)
        if not table:
            return item

        try:
            data = dict(item)
            self.client.table(table).upsert(data, on_conflict="url").execute()
        except Exception as e:
            spider.logger.error(f"Error saving to Supabase: {e}")

        return item

    def _get_table_name(self, item):
        class_name = type(item).__name__
        mapping = {
            "ArticleItem": "articles",
            "EventItem": "events",
            "BusinessItem": "businesses",
            "ProductItem": "products",
            "PlanItem": "plans",
        }
        return mapping.get(class_name)
