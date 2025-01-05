# devto.py

`devto` is a modern Python API client for the Forem API V1, written with `aiohttp` and `pydantic`.

At the moment, functionality only allows one to query articles and publish/update an existing article.


## Installation

Currently there are no Pypi wheels, use

```bash
pip install git+https://github.com/AlejandroGomezFrieiro/devto_py.git
```

## Usage

```python
from devto.client import DevtoClient
from devto.models import DevtoArticle
import asyncio

# Get published articles
async def main():
    async with DevtoClient() as client:
        return await client.published_articles()
asyncio.run(main())

async def publish_article(article):
    async with DevtoClient(api_key = "<API_KEY>") as client:
        return await client.publish_article(article)
article = DevtoArticle(
    title="title",
    body_markdown="Article body"
)
asyncio.run(publish_article(article))

async def edit_article(article):
    async with DevtoClient(api_key = "<API_KEY>") as client:
        return await client.update_article(article)

asyncio.run(edit_article(article))
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
