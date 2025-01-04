import pytest
from devto_api.models import DevtoApi, DevtoArticle


def test_devto_api():
    api = DevtoApi()
    assert api.timeout == 10
    assert api.api_key == None
