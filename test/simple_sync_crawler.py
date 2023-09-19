
from pprint import pprint

from pydantic import HttpUrl

from crawler import SimpleSyncCrawler
from models import CrawlerConfig
from storage import DiskPageStorage

if __name__ == "__main__":
    config = CrawlerConfig(
        entrypoint=HttpUrl(
            "https://example.com"
        ),
        content_type="md",
        from_root=True,
    )
    storage = DiskPageStorage()
    crawler = SimpleSyncCrawler(config=config, storage=storage)
    crawler.run()
    pprint(len(crawler.page_storage))
    print(*crawler.page_storage.keys, sep="\n")
    page = storage.get(
        "0960dcbbbe3fb7cb94aa9eefab9cb5e63d5c1d0a07e61fcac9713545d322d91d")
    if page:
        print(page.url)
