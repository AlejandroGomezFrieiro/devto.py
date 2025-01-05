import asyncio

from devto.client import DevtoClient
from devto.models import DevtoArticle


def test_published_articles():
    async def f(per_page):
        async with DevtoClient() as client:
            return await client.published_articles(per_page=per_page)

    articles = asyncio.run(f(1))
    assert len(articles) == 1
    assert isinstance(articles[0], DevtoArticle)
