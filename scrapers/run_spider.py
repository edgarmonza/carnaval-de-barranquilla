#!/usr/bin/env python3
"""
Script para ejecutar scrapers individuales.
Uso: python run_spider.py <spider_name> [--output file.jsonl]
"""
import sys
import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    if len(sys.argv) < 2:
        print("Uso: python run_spider.py <spider_name>")
        print("\nSpiders disponibles:")
        print("  elheraldo       - Noticias de El Heraldo")
        print("  eluniversal     - Noticias de El Universal")
        print("  carnaval_oficial - Eventos del sitio oficial")
        sys.exit(1)

    spider_name = sys.argv[1]

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    settings = get_project_settings()

    # Override output if specified
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]
            settings["FEEDS"] = {
                output_file: {"format": "jsonlines", "encoding": "utf-8"}
            }

    # Create output directory
    os.makedirs("output", exist_ok=True)

    process = CrawlerProcess(settings)
    process.crawl(spider_name)
    process.start()


if __name__ == "__main__":
    main()
