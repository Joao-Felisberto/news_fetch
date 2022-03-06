from datetime import datetime

import pytest

from db.DBManager import DBManager
from db.objects.article_header import ArticleHeader


@pytest.fixture
def db():
    # return DBManager("tests/test_db.db")
    res = DBManager("/home/me/PycharmProjects/news/tests/db.db")
    # res.reset_test_db()
    return res


def test_store(db):
    assert db.get_table_size("article_headers") == 0

    # db_manager, post_date, title, link
    art1 = ArticleHeader(db, datetime.strptime("2021-01-3117:00:56", "%Y-%m-%d%H:%M:%S"), "Something is working",
                         "https://link.site")
    art2 = ArticleHeader(db, datetime.strptime("2021-02-1510:00:00", "%Y-%m-%d%H:%M:%S"), "Another is working",
                         "https://yeet.site")
    art3 = ArticleHeader(db, datetime.strptime("2021-03-2107:00:45", "%Y-%m-%d%H:%M:%S"), "This final thing is working",
                         "https://another_link.site")

    art1.to_db()
    assert db.get_table_size("article_headers") == 1

    art2.to_db()
    assert db.get_table_size("article_headers") == 2

    art3.to_db()
    assert db.get_table_size("article_headers") == 3


def test_delete(db):
    art1 = ArticleHeader(db, datetime.strptime("2021-01-3117:00:56", "%Y-%m-%d%H:%M:%S"), "Something is working",
                         "https://link.site")
    art1.to_db()
    assert db.get_table_size("article_headers") == 1

    db.delete(art1)
    assert db.get_table_size("article_headers") == 0


def test_get_header_by_id(db):
    art1 = ArticleHeader(db, datetime.strptime("2021-01-3117:00:56", "%Y-%m-%d%H:%M:%S"), "Something is working",
                         "https://link.site")
    art1.to_db()

    assert db.get_header_by_id(0) == art1
