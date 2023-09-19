from .base import PageStorage
from .disk_storage import DiskPageStorage
from .in_memory_storage import InMemoryPageStorage

__all__ = [
    "PageStorage",
    "InMemoryPageStorage",
    "DiskPageStorage",
]
