from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, Field


class PageContent(BaseModel):
    url: AnyHttpUrl
    content: str
    digest: str
    type: Literal["md", "html"]
    links: list[AnyHttpUrl]
    processed: bool = False
    meta: dict[str, str] = Field(default_factory=dict)
