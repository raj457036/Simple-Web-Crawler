from abc import ABC, abstractmethod, abstractproperty
from typing import Callable

from webcrawler.models.page_content import PageContent


class PageStorage(ABC):
    def __init__(self, key_prop: Callable[[PageContent], str] | None = None) -> None:

        if key_prop is None:
            def _(page: PageContent) -> str:
                return page.digest
            key_prop = _

        super().__init__()
        self.key_prop = key_prop

    def setup(self):
        pass

    async def asetup(self):
        pass

    @abstractmethod
    def save(self, page: PageContent) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def asave(self, page: PageContent) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> PageContent | None:
        raise NotImplementedError

    @abstractmethod
    async def aget(self, key: str) -> PageContent | None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[PageContent]:
        raise NotImplementedError

    @abstractmethod
    async def aget_all(self) -> list[PageContent]:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractproperty
    def keys(self) -> list[str]:
        raise NotImplementedError
