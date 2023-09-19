from typing import Literal

from pydantic import BaseModel, HttpUrl


class CrawlerConfig(BaseModel):
    """Crawler configuration model."""

    entrypoint: HttpUrl
    url_prefix_lock: bool = True
    from_root: bool = False
    max_links: int | None = None
    verify_ssl: bool = True
    # depth: int | None = None
    user_agent: str = "*"
    output_type: Literal["md", "html"] = "md"

    # Wait for a maximum of `timeout` seconds for a response. 'None' means no timeout
    timeout: int | None = 25
