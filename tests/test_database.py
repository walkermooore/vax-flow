from pytest import raises

from app import db, error


def test_pop_db_sucess():
    assert db.pop_db() == None
