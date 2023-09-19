# Simple Web Crawler

A performant but simple web crawler thats easy to use and extend, supports async and sync requests with in memory and disk caching for high performance.

## Installation

```bash
pip install --upgrade git+https://github.com/raj457036/Simple-Web-Crawler.git@main
```

## Usage

```python
from pydantic import HttpUrl

from simple_crawler import SimpleSyncCrawler, CrawlerConfig, InMemoryPageStorage

# Create a crawler with a config and storage
config = CrawlerConfig(
    entrypoint=HttpUrl(
        "https://example.com"
    ),
    content_type="md",
    from_root=True,
)
# In memory storage
# you can also try `DiskPageStorage` for persistent storage and heavy volume.
storage = InMemoryPageStorage()

# Run the crawler
crawler = SimpleSyncCrawler(config=config, storage=storage)
crawler.run()

# Print the results or do something else with them
print(*crawler.page_storage.keys, sep="\n")
```

## Features

- [x] Sync and Async requests
- [x] In memory and disk storage
- [x] Configurable
- [x] Pydantic and type annotated
- [x] Extensible
- [x] Customizable
- [x] High performance
- [x] Easy to use
