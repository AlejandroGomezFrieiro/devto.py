# devto_api

`devto` is a modern Python API client for the Forem API V1, written with `aiohttp` and `pydantic`.


## Installation

Currently there are no Pypi wheels, use

```bash
pip install git+https://github.com/AlejandroGomezFrieiro/devto_py.git
```

## Usage

```python
from devto import DevtoClient
import asyncio

async def main():
    async with DevtoClient() as client:
        return await client.published_articles()
asyncio.run(main())
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
