import os

from fastapi.testclient import TestClient
from pytest import fixture, raises

from app import app, core, error, util


@fixture
def exception_422():
    yield error.CustomHTTPException(422)


def test_custom_exception():
    e = error.CustomHTTPException(422)

    assert e.detail == "Unprocessable Entity"


from fastapi.testclient import TestClient

from app import app, core, error, util

client = TestClient(app)


def test_custom_http_exception(exception_422):
    from fastapi import HTTPException

    with raises(HTTPException) as e:
        error.CustomHTTPException(exception_422)

    assert e.value.detail == "Unprocessable Entity"
