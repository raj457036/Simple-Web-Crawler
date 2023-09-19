from abc import ABC, abstractmethod

from models.crawler_config import CrawlerConfig
from storage import PageStorage


class __Crawler(ABC):
    def __init__(self, config: CrawlerConfig) -> None:
        super().__init__()
        self.config = config


class AbstractSyncCrawler(__Crawler):
    def __init__(self, *, config: CrawlerConfig, storage: PageStorage) -> None:
        super().__init__(config)
        self.page_storage: PageStorage = storage

    @abstractmethod
    def run(self) -> None:
        self.page_storage.setup()


class AbstractAsyncCrawler(__Crawler):
    def __init__(self, *, config: CrawlerConfig, storage: PageStorage) -> None:
        super().__init__(config)
        self.page_storage: PageStorage = storage

    @abstractmethod
    async def run(self) -> None:
        await self.page_storage.asetup()
