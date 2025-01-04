from typing import Any, Literal, Optional, TypeAlias

import requests
from loguru import logger
from pydantic import BaseModel, HttpUrl, SecretStr

from .models import DevtoArticle

ApiKey: TypeAlias = SecretStr
Header: TypeAlias = dict[str, Any]


class ApiWrapper(BaseModel):
    url: HttpUrl = HttpUrl(url="https://dev.to/api/")
    api_key: Optional[ApiKey] = None
    timeout: int = 10


class DevtoApi(ApiWrapper):
    @property
    def header(self):
        return {
            "Accept": "application/vnd.forem.api-v1+json",
            "Content-Type": "application/json",
            "api-key": self.api_key.get_secret_value()
            if self.api_key is not None
            else "",
        }

    def get(self, endpoint: str, **kwargs):
        return requests.get(
            url=HttpUrl(self.url.unicode_string() + endpoint).unicode_string(),
            headers=self.header,
            timeout=self.timeout,
            params=kwargs,
        )

    def published_articles(
        self,
        page: int = 1,
        per_page: int = 30,
        tag: Optional[str] = None,
        tags: Optional[str] = None,
        tags_exclude: Optional[str] = None,
        username: Optional[str] = None,
        state: Optional[Literal["fresh", "rising", "all"]] = None,
        top: Optional[int] = None,
        collection_id: Optional[int] = None,
    ) -> list[DevtoArticle]:
        logger.debug(f"GET: {str(HttpUrl(str(self.url) + 'articles'))}")
        response = self.get(
            "articles",
            page=page,
            per_page=per_page,
            tag=tag,
            tags=tags,
            username=username,
            state=state,
            top=top,
            collection_id=collection_id,
        )
        return [DevtoArticle(**article) for article in response.json()]

    def get_all_articles(
        self,
        page: int = 1,
        per_page: int = 30,
        tag: Optional[str] = None,
        tags: Optional[str] = None,
        tags_exclude: Optional[str] = None,
        username: Optional[str] = None,
        state: Optional[Literal["fresh", "rising", "all"]] = None,
        top: Optional[int] = None,
        collection_id: Optional[int] = None,
    ) -> list[DevtoArticle]:
        response = self.get(
            "articles/me/all",
            page=page,
            per_page=per_page,
            tag=tag,
            tags=tags,
            username=username,
            state=state,
            top=top,
            collection_id=collection_id,
        )

        return [DevtoArticle(**article) for article in response.json()]

    def update_article(self, article: DevtoArticle) -> None:
        logger.debug(f"Pushing payload {article.to_payload}")
        response = requests.put(
            url=str(HttpUrl(str(self.url) + f"articles/{article.id}")),
            headers=self.header,
            json=article.to_payload(),
            timeout=self.timeout,
        )
        match response.status_code:
            case 201:
                logger.debug("Article published")
                logger.debug("Response:", response.json())
            case 401:
                raise requests.exceptions.HTTPError("Unauthorized.")
            case 404:
                raise requests.exceptions.HTTPError("Article not found.")
            case 402:
                raise requests.exceptions.HTTPError("Unprocessable entry.")

    def publish_article(self, article: DevtoArticle) -> None:
        logger.debug(f"Pushing payload {article.to_payload}")
        response = requests.post(
            url=str(HttpUrl(str(self.url) + "articles")),
            headers=self.header,
            json=article.to_payload(),
            timeout=self.timeout,
        )
        match response.status_code:
            case 201:
                logger.debug("Article published")
                logger.debug("Response:", response.json())
            case 401:
                raise requests.exceptions.HTTPError("Unauthorized.")
            case 402:
                raise requests.exceptions.HTTPError("Unprocessable entry.")
