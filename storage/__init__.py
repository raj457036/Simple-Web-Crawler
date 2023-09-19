from storage.base import PageStorage
from storage.disk_storage import DiskPageStorage
from storage.in_memory_storage import InMemoryPageStorage

__all__ = [
    "PageStorage",
    "InMemoryPageStorage",
    "DiskPageStorage",
]
