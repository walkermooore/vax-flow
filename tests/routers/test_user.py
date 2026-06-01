import pytest

from app import models, schema, util


@pytest.fixture(scope="module")
def test_user():
    dict_data = {
        "nome_usuario": util.generate_fake_data("nome_usuario"),
        "email": util.generate_fake_data("email"),
        "senha": util.generate_fake_data("senha"),
        "active": util.generate_fake_data("bool"),
    }
    schema_data = schema.PostUser(**dict_data)
    user = models.Usuarios(**schema_data.model_dump())
    user = user.create()
    yield user


def test_get_user(test_client):
    response = test_client.get("/api/v1/user/?all=true&operator=%3D&skip=0&limit=100")
    assert response.status_code == 200


def test_create_user(test_client):
    response = test_client.post(
        "/api/v1/user",
        json={
            "nome_usuario": util.generate_fake_data("nome_usuario"),
            "email": util.generate_fake_data("email"),
            "senha": util.generate_fake_data("senha"),
            "active": util.generate_fake_data("bool"),
        },
    )
    assert response.status_code == 201


def test_patch_user(test_client, test_user):
    response = test_client.patch(
        f"/api/v1/user/?uuid={test_user.id}",
        json={
            "nome_usuario": util.generate_fake_data("nome_usuario"),
            "email": util.generate_fake_data("email"),
            "senha": util.generate_fake_data("senha"),
            "active": util.generate_fake_data("bool"),
        },
    )
    assert response.status_code == 200


def test_delete_user(test_client, test_user):
    response = test_client.delete(f"/api/v1/user/?uuid={test_user.id}")
    assert response.status_code == 200
