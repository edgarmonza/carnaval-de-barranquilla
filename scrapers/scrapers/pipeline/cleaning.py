import re
from datetime import datetime, timezone


class CleaningPipeline:
    """Limpia y normaliza los datos scrapeados."""

    def process_item(self, item, spider):
        # Add scraped_at timestamp
        if not item.get("scraped_at"):
            item["scraped_at"] = datetime.now(timezone.utc).isoformat()

        # Clean whitespace from all string fields
        for field in item.fields:
            value = item.get(field)
            if isinstance(value, str):
                item[field] = self._clean_text(value)

        return item

    def _clean_text(self, text: str) -> str:
        text = text.strip()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text
