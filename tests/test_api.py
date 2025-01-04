from devto_api.api import DevtoApi


def test_get_all_articles():
    api = DevtoApi()
    assert len(api.published_articles(per_page=1)) == 1
