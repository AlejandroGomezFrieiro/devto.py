import requests
import json
import os
from pydantic import BaseModel, Field
from typing import Optional


class DevtoArticle(BaseModel):
    """
    Pydantic model corresponding to an article.
    """

    title: str
    body_markdown: str = Field(default="")
    published: Optional[bool] = None
    series: Optional[str] = None
    main_image: Optional[str] = None
    canonical_url: Optional[str] = None
    description: Optional[str] = None
    tags: list[str] = Field(default_factory=lambda: [])
    organization: Optional[str] = None

    def to_payload(self) -> dict[str, dict[str, any]]:
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


class DevtoApi(BaseModel):
    """
    Pydantic model containing the DevtoApi.
    """

    api_key: Optional[str] = None
    timeout: int = 10
    header: Optional[dict[str, str]] = None

    def model_post_init(self, _context):
        self.header = {"Content-Type": "application/json", "api-key": self.api_key}

    def publish_article(self, article: DevtoArticle) -> None:
        print(article.to_payload())
        response = requests.post(
            url="https://dev.to/api/articles",
            headers=self.header,
            json=article.to_payload(),
            timeout=self.timeout,
        )
        match response.status_code:
            case 201:
                print("Article published")
                print("Response:", response.json())
            case _:
                print(f"Error. Status code: {response.status_code}")
