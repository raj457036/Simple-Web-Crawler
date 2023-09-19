from functools import lru_cache
from urllib.parse import urlparse
from urllib.robotparser import RequestRate, RobotFileParser

import httpx


class RobotParser:
    def __init__(self, url: str, user_agent: str = "*") -> None:
        uri = urlparse(url)
        self.user_agent = user_agent
        self.url = f"{uri.scheme}://{uri.netloc}/robots.txt"
        self.__fp = RobotFileParser()

    async def aread(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url)
            self.__fp.parse(response.text.splitlines())

    def read(self):
        with httpx.Client() as client:
            response = client.get(self.url)
            self.__fp.parse(response.text.splitlines())

    @lru_cache()
    def can_fetch(self, url: str, user_agent: str | None = None) -> bool:
        user_agent = user_agent or self.user_agent
        return self.__fp.can_fetch(user_agent, url)

    @lru_cache()
    def request_rate(self, user_agent: str | None = None) -> (RequestRate | None):
        user_agent = user_agent or self.user_agent
        return self.__fp.request_rate(user_agent)

    def crawl_delay(self, user_agent: str | None = None) -> (int | None):
        user_agent = user_agent or self.user_agent
        if seconds := self.__fp.crawl_delay(user_agent):
            return int(seconds)
        return None
