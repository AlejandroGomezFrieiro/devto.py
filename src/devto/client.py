from typing import Any, Literal, Optional, Self, TypeAlias

import aiohttp
from aiohttp_client_cache.backends.sqlite import SQLiteBackend
from aiohttp_client_cache.session import CachedSession
from loguru import logger
from pydantic import BaseModel, HttpUrl, SecretStr

from .models import DevtoArticle

__all__ = ["DevtoClient"]

ApiKey: TypeAlias = SecretStr
Header: TypeAlias = dict[str, Any]


class DevtoClient:
    BASE_URL = "https://dev.to/api/"

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        headers: Optional[Header] = None,
        cache_path: str = "./.cache/hakushin/aiohttp-cache.db",
        cache_ttl: int = 3600,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self._session = session
        self._cache = SQLiteBackend(cache_path, expire_after=cache_ttl)
        self._api_key = SecretStr(api_key) if api_key is not None else None
        self._headers = headers or {
            "Accept": "application/vnd.forem.api-v1+json",
            "Content-Type": "application/json",
            "api-key": self._api_key.get_secret_value()
            if self._api_key is not None
            else "",
        }

    async def update_article(
        self,
        article: DevtoArticle,
        use_cache: bool = True,
    ):
        logger.debug(f"Publishing article {article}")
        response = await self._post(
            f"articles/{article.id}", data=article, use_cache=use_cache
        )
        return response

    async def publish_article(
        self,
        article: DevtoArticle,
        use_cache: bool = True,
    ):
        logger.debug(f"Publishing article {article}")
        response = await self._put("articles", data=article, use_cache=use_cache)
        return response

    async def published_articles(
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
        use_cache: bool = True,
    ) -> dict[str, Any]:
        data = await self._get(
            "articles",
            use_cache,
            page=page,
            per_page=per_page,
            tag=tag,
            tags=tags,
            tags_exclude=tags_exclude,
            username=username,
            state=state,
            top=top,
            collection_id=collection_id,
        )
        logger.debug(f"Data is {data}")

        # return data
        return [DevtoArticle(**article) for article in data]

    async def _put(
        self, endpoint: str, data: BaseModel, use_cache: bool, **kwargs
    ) -> dict[str, Any]:
        if self._session is None:
            raise RuntimeError("Use `start` before making requests.")

        request_url = HttpUrl(self.BASE_URL + endpoint).unicode_string()
        logger.debug(f"PUT: {request_url}")

        payload = data.model_dump()

        logger.debug(f"payload: {payload}")
        if not use_cache and isinstance(self._session, CachedSession):
            async with (
                self._session.disabled(),
                self._session.post(request_url, json=payload) as resp,
            ):
                logger.debug(resp.status)
                match resp.status:
                    case resp.status if 200 <= resp.status <= 299:
                        return await resp.json()
                    case _:
                        raise ValueError("Error posting the data")
        else:
            async with self._session.post(request_url, json=payload) as resp:
                logger.debug(resp.status)
                match resp.status:
                    case resp.status if 200 <= resp.status <= 299:
                        return await resp.json()
                    case _:
                        raise ValueError("Error posting the data")

    async def _post(
        self, endpoint: str, data: BaseModel, use_cache: bool, **kwargs
    ) -> dict[str, Any]:
        if self._session is None:
            raise RuntimeError("Use `start` before making requests.")

        request_url = HttpUrl(self.BASE_URL + endpoint).unicode_string()
        logger.debug(f"POST: {request_url}")

        payload = data.model_dump()

        logger.debug(f"payload: {payload}")
        if not use_cache and isinstance(self._session, CachedSession):
            async with (
                self._session.disabled(),
                self._session.post(request_url, json=payload) as resp,
            ):
                logger.debug(resp.status)
                match resp.status:
                    case resp.status if 200 <= resp.status <= 299:
                        return await resp.json()
                    case _:
                        raise ValueError("Error posting the data")
        else:
            async with self._session.post(request_url, json=payload) as resp:
                logger.debug(resp.status)
                match resp.status:
                    case resp.status if 200 <= resp.status <= 299:
                        return await resp.json()
                    case _:
                        raise ValueError("Error posting the data")

    async def _get(self, endpoint: str, use_cache: bool, **kwargs) -> dict[str, Any]:
        if self._session is None:
            raise RuntimeError("Use `start` before making requests.")

        request_url = HttpUrl(self.BASE_URL + endpoint).unicode_string()
        logger.debug(f"GET: {request_url}")

        kwargs = {key: value for key, value in kwargs.items() if value is not None}

        if not use_cache and isinstance(self._session, CachedSession):
            async with (
                self._session.disabled(),
                self._session.get(request_url, params=kwargs) as resp,
            ):
                logger.debug(resp.status)
                match resp.status:
                    case resp.status if 200 <= resp.status <= 299:
                        data = await resp.json()
                    case _:
                        raise ValueError("Error fetching the data.")
        else:
            async with self._session.get(request_url, params=kwargs) as resp:
                logger.debug(resp.status)
                match resp.status:
                    case resp.status if 200 <= resp.status <= 299:
                        data = await resp.json()
                    case _:
                        raise ValueError("Error fetching the data.")

        return data

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        await self.close()

    async def start(self) -> None:
        headers = self._headers
        logger.debug(f"headers: {headers}")
        self._session = self._session or CachedSession(
            headers=headers, cache=self._cache
        )

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()


#
#     def published_articles(
#         self,
#         page: int = 1,
#         per_page: int = 30,
#         tag: Optional[str] = None,
#         tags: Optional[str] = None,
#         tags_exclude: Optional[str] = None,
#         username: Optional[str] = None,
#         state: Optional[Literal["fresh", "rising", "all"]] = None,
#         top: Optional[int] = None,
#         collection_id: Optional[int] = None,
#     ) -> list[DevtoArticle]:
#         logger.debug(f"GET: {str(HttpUrl(str(self.url) + 'articles'))}")
#         response = self.get(
#             "articles",
#             page=page,
#             per_page=per_page,
#             tag=tag,
#             tags=tags,
#             username=username,
#             state=state,
#             top=top,
#             collection_id=collection_id,
#         )
#         return [DevtoArticle(**article) for article in response.json()]
#
#     def get_all_articles(
#         self,
#         page: int = 1,
#         per_page: int = 30,
#         tag: Optional[str] = None,
#         tags: Optional[str] = None,
#         tags_exclude: Optional[str] = None,
#         username: Optional[str] = None,
#         state: Optional[Literal["fresh", "rising", "all"]] = None,
#         top: Optional[int] = None,
#         collection_id: Optional[int] = None,
#     ) -> list[DevtoArticle]:
#         response = self.get(
#             "articles/me/all",
#             page=page,
#             per_page=per_page,
#             tag=tag,
#             tags=tags,
#             username=username,
#             state=state,
#             top=top,
#             collection_id=collection_id,
#         )
#
#         return [DevtoArticle(**article) for article in response.json()]
#
#     def update_article(self, article: DevtoArticle) -> None:
#         logger.debug(f"Pushing payload {article.to_payload}")
#         response = requests.put(
#             url=str(HttpUrl(str(self.url) + f"articles/{article.id}")),
#             headers=self.header,
#             json=article.to_payload(),
#             timeout=self.timeout,
#         )
#         match response.status_code:
#             case 201:
#                 logger.debug("Article published")
#                 logger.debug("Response:", response.json())
#             case 401:
#                 raise requests.exceptions.HTTPError("Unauthorized.")
#             case 404:
#                 raise requests.exceptions.HTTPError("Article not found.")
#             case 402:
#                 raise requests.exceptions.HTTPError("Unprocessable entry.")
#
#     def publish_article(self, article: DevtoArticle) -> None:
#         logger.debug(f"Pushing payload {article.to_payload}")
#         response = requests.post(
#             url=str(HttpUrl(str(self.url) + "articles")),
#             headers=self.header,
#             json=article.to_payload(),
#             timeout=self.timeout,
#         )
#         match response.status_code:
#             case 201:
#                 logger.debug("Article published")
#                 logger.debug("Response:", response.json())
#             case 401:
#                 raise requests.exceptions.HTTPError("Unauthorized.")
#             case 402:
#                 raise requests.exceptions.HTTPError("Unprocessable entry.")
