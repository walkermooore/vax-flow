import os

from fastapi import UploadFile
from pytest import fixture, mark, raises

from app import auth, error, models, util


@fixture(scope="module")
def test_login(test_client):
    response = test_client.post(
        "/api/v1/login/access-token",
        data={
            "nome_usuario": "admin",
            "senha": "admin",
        },
    )
    token = response.json().get("token")
    yield token


@fixture
def sub():
    yield {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "key": [1, 2, 3, 4],
    }


@fixture
def sub_invalido():
    yield {"user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}


@fixture
def user_token_invalido(sub_invalido):
    yield auth.encode_token(sub_invalido, 20)


@fixture
def user_token(sub):
    yield auth.encode_token(sub, 20)


@fixture
def token():
    yield auth.encode_token("sub", 20)


def test_encode_token_token_valido(sub):
    assert type(auth.encode_token(sub, 20)) == str
