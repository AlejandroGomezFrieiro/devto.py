from devto_api.api import DevtoApi


def test_devto_api():
    api = DevtoApi()
    assert api.timeout == 10
    assert api.api_key is None
