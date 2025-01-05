from devto.models import DevtoArticle


def test_devto_article():
    article = DevtoArticle(title="test", body_markdown="test markdown")

    assert "article" in article.model_dump()
    assert article.model_dump() == {
        "article": {"title": "test", "body_markdown": "test markdown"}
    }
