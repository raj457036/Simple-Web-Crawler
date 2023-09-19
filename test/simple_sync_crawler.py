
from pydantic import HttpUrl

from webcrawler import (CrawlerConfig, InMemoryPageStorage,  # ,DiskPageStorage
                        SimpleSyncCrawler)

if __name__ == "__main__":
    config = CrawlerConfig(
        entrypoint=HttpUrl(
            "https://github.com"
        ),
        output_type="md",
        from_root=True,
        max_links=100,
    )
    storage = InMemoryPageStorage()
    crawler = SimpleSyncCrawler(config=config, storage=storage)
    crawler.run()
    # pprint(len(crawler.page_storage))
    # print(*crawler.page_storage.keys, sep="\n")
    page = storage.get(crawler.page_storage.keys[0])
    if page:
        print(page.url)
