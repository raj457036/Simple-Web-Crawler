from typing import Literal

from pydantic import BaseModel, HttpUrl


class CrawlerConfig(BaseModel):
    """Crawler configuration model."""

    entrypoint: HttpUrl
    url_prefix_lock: bool = True
    from_root: bool = False
    max_links: int | None = None
    verify_ssl: bool = True
    disable_verify_ssl_on_fail: bool = False
    depth: int | None = None
    user_agent: str = "*"
    content_type: Literal["md", "html"] = "md"

    # Wait for a maximum of 10 seconds for a response. 'None' means no timeout
    timeout: int | None = 10
