import asyncio
from pathlib import Path
from typing import Callable

import aiofiles as aiof
from pydantic.version import VERSION
from typing_extensions import override

from webcrawler.logger import logger as root_logger
from webcrawler.models.page_content import PageContent
from webcrawler.storage.base import PageStorage


class DiskPageStorage(PageStorage):
    def __init__(
        self,
        key_prop: Callable[[PageContent], str] | None = None,
        storage_dir: str = "crawled_pages",
    ) -> None:
        super().__init__(key_prop)
        self.storage_dir = Path(storage_dir)
        self.storage_keys: set[str] = set()

    @override
    def setup(self):
        root_logger.debug("Setting up storage")
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        # list all files in storage_dir
        for file in self.storage_dir.iterdir():
            if file.is_file():
                self.storage_keys.add(file.name)

    @override
    async def asetup(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.setup)

    @override
    def save(self, page: PageContent) -> bool:
        key = self.key_prop(page)
        self.storage_keys.add(str(key))
        with open(self.storage_dir / key, "w") as f:
            dumps: str = getattr(page, "json")() if VERSION.startswith(
                "1.10") else page.model_dump_json()
            f.write(dumps)
        return True

    @override
    async def asave(self, page: PageContent) -> bool:
        key = self.key_prop(page)
        self.storage_keys.add(key)
        async with aiof.open(self.storage_dir / key, "w") as f:
            if VERSION.startswith("1.10"):
                dumps: str = getattr(page, "json")()
            else:
                dumps: str = page.model_dump_json()
            await f.write(dumps)
        return True

    @override
    def get(self, key: str) -> PageContent | None:
        try:
            with open(self.storage_dir / str(key), "r") as f:
                if VERSION.startswith("1.10"):
                    return getattr(PageContent, 'parse_raw')(f.read())
                return PageContent.model_validate_json(f.read())
        except Exception as e:
            root_logger.error(f"Error while reading {key}: {e}")
            return None

    @override
    async def aget(self, key: str) -> PageContent | None:
        try:
            async with aiof.open(self.storage_dir / str(key), "r") as f:
                if VERSION.startswith("1.10"):
                    return getattr(PageContent, 'parse_raw')(await f.read())
                return PageContent.model_validate_json(await f.read())
        except Exception as e:
            root_logger.error(f"Error while reading {key}: {e}")
            return None

    @override
    def get_all(self) -> list[PageContent]:
        pages: list[PageContent] = []
        for key in self.storage_keys:
            if page := self.get(key):
                pages.append(page)
        return pages

    @override
    async def aget_all(self) -> list[PageContent]:
        pages: list[PageContent] = []
        for key in self.storage_keys:
            if page := await self.aget(key):
                pages.append(page)
        return pages

    @property
    @override
    def keys(self) -> list[str]:
        return list(self.storage_keys)

    @override
    def __len__(self) -> int:
        return len(self.storage_keys)
