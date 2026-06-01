import pytest

from app import models, schema, util


@pytest.fixture(scope="module")
def test_role():
    dict_data = {
        "name": util.generate_fake_data("name"),
        "access_level": util.generate_fake_data("int"),
        "description": util.generate_fake_data("str"),
    }
    schema_data = schema.PostRole(**dict_data)
    role = models.Role(**schema_data.model_dump())
    role = role.create()
    yield role


def test_get_role(test_client):
    response = test_client.get("/api/v1/role/?all=true&operator=%3D&skip=0&limit=100")
    assert response.status_code == 200


def test_create_role(test_client):
    response = test_client.post(
        "/api/v1/role",
        json={
            "name": util.generate_fake_data("name"),
            "access_level": util.generate_fake_data("int"),
            "description": util.generate_fake_data("str"),
        },
    )
    assert response.status_code == 201


def test_patch_role(test_client, test_role):
    response = test_client.patch(
        f"/api/v1/role/?uuid={test_role.id}",
        json={
            "name": util.generate_fake_data("name"),
            "access_level": util.generate_fake_data("int"),
            "description": util.generate_fake_data("str"),
        },
    )
    assert response.status_code == 200


def test_delete_role(test_client, test_role):
    response = test_client.delete(f"/api/v1/role/?uuid={test_role.id}")
    assert response.status_code == 200
