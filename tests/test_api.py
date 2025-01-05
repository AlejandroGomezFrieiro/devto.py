import asyncio

from devto.client import DevtoClient


def test_published_articles():
    async def f():
        async with DevtoClient() as client:
            return await client.published_articles()

    articles = asyncio.run(f())
    assert len(articles) == 30
