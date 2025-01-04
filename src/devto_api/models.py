from typing import Any, Optional

from pydantic import BaseModel, Field


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

    id: Optional[int] = None
    published: Optional[bool] = None
    series: Optional[str] = None
    main_image: Optional[str] = None
    canonical_url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None  # = Field(default_factory=lambda: [])
    organization: Optional[dict] = None

    # @model_validator(mode="after")
    # def check_tags(self) -> Self:
    #     if len(self.tags) > 4:
    #         raise ValueError("DevTo only acepts a maximum of 4 tags per article.")
    #     return self

    def to_payload(self) -> dict[str, dict[str, Any]]:
        """
        Convert the model to a payload that can be sent through post.
        """
        return {
            "article": {
                key: value
                for key, value in self.model_dump().items()
                if value is not None
            }
        }
