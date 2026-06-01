import pytest

from app import models, schema, util


@pytest.fixture(scope="module")
def user():
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


@pytest.fixture(scope="module")
def role():
    dict_data = {
        "name": util.generate_fake_data("name"),
        "access_level": util.generate_fake_data("int"),
        "description": util.generate_fake_data("str"),
    }
    schema_data = schema.PostRole(**dict_data)
    role = models.Role(**schema_data.model_dump())
    role = role.create()
    yield role


@pytest.fixture(scope="module")
def test_user_role(role, user):
    dict_data = {
        "user_id": str(user.id),
        "role_id": str(role.id),
    }
    schema_data = schema.PostUserRole(**dict_data)
    user_role = models.UserRole(**schema_data.model_dump())
    user_role = user_role.create()
    yield user_role


def test_get_user_role(test_client):
    response = test_client.get(
        "/api/v1/user-role/?all=true&operator=%3D&skip=0&limit=100"
    )
    assert response.status_code == 200


def test_create_user_role(test_client, user, role):
    response = test_client.post(
        "/api/v1/user-role",
        json={
            "user_id": str(user.id),
            "role_id": str(role.id),
        },
    )
    assert response.status_code == 201


def test_patch_user_role(test_client, test_user_role, role, user):
    response = test_client.patch(
        f"/api/v1/user-role/?uuid={test_user_role.id}",
        json={
            "user_id": str(user.id),
            "role_id": str(role.id),
        },
    )
    assert response.status_code == 200


def test_delete_user_role(test_client, test_user_role):
    response = test_client.delete(f"/api/v1/user-role/?uuid={test_user_role.id}")
    assert response.status_code == 200
