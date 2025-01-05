from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, model_serializer

__all__ = ["DevtoArticle", "ArticleBody"]


class ArticleBody(BaseModel):
    """Pydantic model representing an arbitrary article or blogpost with a title and a markdown body.

    Attributes:
        title: Title of the article
        body_markdown: Contents of the article in markdown.
    """

    title: str
    body_markdown: str = Field(default="")


class DevtoArticle(ArticleBody):
    """Pydantic model representing a devto article.

    Attributes:
        published: Whether the article is published or not.
        series: Series the article belongs to.
        main_image: Article image.
        canonical_url: Canonical URL.
        description: Description.
        tags: List of tags.
        organization: Organization the article belongs to.
    """

    model_config = ConfigDict(extra="ignore")
    id: Optional[int] = None
    published: Optional[bool] = None
    series: Optional[str] = None
    main_image: Optional[str] = None
    canonical_url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None  # = Field(default_factory=lambda: [])
    organization: Optional[dict] = None

    @model_serializer
    def article_model(self) -> dict[str, Any]:
        return {"article": {key: value for key, value in self if value is not None}}
