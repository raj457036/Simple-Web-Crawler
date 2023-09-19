import concurrent.futures as fu
import threading
import time
from hashlib import sha256
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from pydantic import AnyHttpUrl
from typing_extensions import override

from crawler.abstract import AbstractSyncCrawler
from crawler.robot_parser import RobotParser
from logger import logger as root_logger
from models.crawler_config import CrawlerConfig
from models.page_content import PageContent
from storage import InMemoryPageStorage, PageStorage
from utils import bf4_to_md


class SimpleSyncCrawler(AbstractSyncCrawler):
    def __init__(self, *, config: CrawlerConfig, storage: PageStorage | None = None) -> None:
        if storage is None:
            storage = InMemoryPageStorage()

        super().__init__(config=config, storage=storage)

        self.robot_parser = RobotParser(
            str(config.entrypoint),
            config.user_agent
        )
        self.client: httpx.Client | None = None
        self.link_set: set[str] = set()
        self.crawled: set[str] = set()
        self.done = threading.Event()

        # link counter
        self.lc = config.max_links or -1

        uri = urlparse(str(self.config.entrypoint))
        self.origin = f"{uri.scheme}://{uri.netloc}"
        if config.from_root:
            self.base_url = self.origin
        else:
            path = Path(uri.path)
            self.base_url = str(
                self.config.entrypoint).removesuffix(path.suffix)

    @override
    def run(self) -> None:
        super().run()
        with httpx.Client(
            verify=self.config.verify_ssl,
            follow_redirects=True,
            timeout=self.config.timeout,
        ) as client:
            root_logger.info("Setting up client")
            self.client = client

            root_logger.info("Reading robots.txt")
            self.robot_parser.read()
            root_logger.info("Reading robots.txt done")

            root_logger.info("Crawling")

            self._init_link_set()

            self.crawl()
            root_logger.info("Crawling done")

            root_logger.info("Tearing down client")
            self.client = None

    def _init_link_set(self) -> None:
        self.add_link(self.base_url)

    def crawl(self):
        while not self.done.is_set():
            if self.link_set:
                with fu.ThreadPoolExecutor() as executor:
                    executor.map(self.read_link, [*self.link_set])
                    self.link_set.clear()
                    executor.shutdown()
            else:
                root_logger.warn("No more links to crawl")
                self.done.set()

    def read_link(self, url: str) -> None:
        assert self.client is not None

        self.respect_rate_limit()

        try:
            response = self.client.get(url)
            root_logger.info(f"Read {url} ✅")
            if response.status_code == 200:
                self.crawled.add(url)
                self.process_link(url, response.content)
        except httpx.HTTPError as e:
            root_logger.error(f"Error reading {url}: {e}")

    def respect_rate_limit(self) -> None:
        self.last_request: float = getattr(self, "last_request", 0)
        self.request_count: int = getattr(self, "request_count", 0)
        now = time.time()
        if now - self.last_request > 1:
            self.last_request = now
            self.request_count = 0
        else:
            self.request_count += 1

        if rate := self.robot_parser.request_rate(self.config.user_agent):
            max_requests_per_second = rate.requests / rate.seconds
            if self.request_count > max_requests_per_second:
                root_logger.warn(
                    f"Rate limit reached, sleeping for {rate.seconds} seconds")
                time.sleep(1)

    def process_link(self, url: str, response: bytes) -> None:
        bf4 = BeautifulSoup(response, "html.parser")
        connected_links: set[AnyHttpUrl] = set()

        for link in bf4.find_all("a"):
            href: str | None = link.get("href")
            if href is not None:
                url_ = self.prepare_url(href)
                connected_links.add(AnyHttpUrl(url_))
                self.add_link(url_)

        self.read_content(url, connected_links, bf4)

    def prepare_url(self, path: str) -> str:
        if path.startswith("/"):
            url = f"{self.origin}{path}"
        elif path.startswith(("http://", "https://")):
            url = path
        else:
            url = f"{self.base_url}/{path}"

        uri = urlparse(url)
        return f"{uri.scheme}://{uri.netloc}{uri.path}".removesuffix("/")

    def add_link(self, url: str) -> None:

        if self.reached_max_links():
            return

        if url in self.link_set:
            return

        if url in self.crawled:
            root_logger.debug(f"✔ Skipping {url} as it is already crawled")
            return

        if not self.robot_parser.can_fetch(url):
            root_logger.debug(
                f"🚫 Skipping {url} as it is not allowed by robots.txt")
            return

        if self.config.url_prefix_lock and not url.startswith(self.base_url):
            root_logger.debug(
                f"⌛︎ Skipping {url} as it is not in the same domain prefix")
            return

        root_logger.debug(f"Adding {url} to link set")
        self.link_set.add(url)
        self.update_link_counter()

    def read_content(
        self,
        url: str,
        connected_links: Iterable[AnyHttpUrl],
        content: BeautifulSoup
    ):

        if self.config.content_type == "md" and (md := bf4_to_md(content)):
            hash = sha256(md.encode("utf-8")).hexdigest()
            page_content = PageContent(
                url=AnyHttpUrl(url),
                content=md,
                type="md",
                digest=hash,
                links=list(connected_links)
            )
            self.page_storage.save(page_content)
        elif self.config.content_type == "html" and (html := str(content)):
            hash = sha256(html.encode("utf-8")).hexdigest()
            page_content = PageContent(
                url=AnyHttpUrl(url),
                content=html,
                type="html",
                digest=hash,
                links=list(connected_links)
            )
            self.page_storage.save(page_content)
        else:
            root_logger.error(f"Could not read content from {url}")

    def update_link_counter(self) -> None:
        if self.config.max_links and self.lc > 0:
            self.lc -= 1

    def reached_max_links(self) -> bool:
        return self.config.max_links is not None and self.lc <= 0
