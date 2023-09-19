from typing import Callable

from typing_extensions import override

from models.page_content import PageContent
from storage.base import PageStorage


class InMemoryPageStorage(PageStorage):
    def __init__(self, key_prop: Callable[[PageContent], str] | None = None) -> None:
        super().__init__(key_prop)
        self.storage: dict[str, PageContent] = {}

    @override
    def save(self, page: PageContent) -> bool:
        key = self.key_prop(page)
        self.storage[key] = page
        return True

    @override
    async def asave(self, page: PageContent) -> bool:
        return self.save(page)

    @override
    def get(self, key: str) -> PageContent | None:
        return self.storage.get(key)

    @override
    async def aget(self, key: str) -> PageContent | None:
        return self.get(key)

    @override
    def get_all(self) -> list[PageContent]:
        return list(self.storage.values())

    @override
    async def aget_all(self) -> list[PageContent]:
        return self.get_all()

    @property
    @override
    def keys(self) -> list[str]:
        return list(self.storage.keys())

    @override
    def __len__(self) -> int:
        return len(self.storage)
