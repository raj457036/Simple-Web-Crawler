from typing import Any, ParamSpecKwargs

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter


def bf4_to_md(soup: BeautifulSoup, **options: ParamSpecKwargs) -> str:
    """Converts a BeautifulSoup object to Markdown."""

    converter = MarkdownConverter(**options)
    result: Any = converter.convert_soup(soup)
    if isinstance(result, str):
        return result
    return ""
