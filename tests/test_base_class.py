import pytest
from fastapi import HTTPException

from app import error, models, schema, util
from app.db.base_class import Response


@pytest.fixture(scope="module")
def test_inactive_user():
    inactive_user = models.Usuarios.get("nome_usuario", "nome_usuario")
    if inactive_user:
        if not inactive_user.active:
            yield inactive_user
    else:
        dict_data = {
            "nome_usuario": "nome_usuario",
            "email": util.generate_fake_data("email"),
            "senha": "senha",
            "active": False,
        }
        schema_data = schema.PostUser(**dict_data)
        user = models.Usuarios(**schema_data.model_dump())
        inactive_user = user.create()
        yield inactive_user


@pytest.fixture(scope="module")
def test_base_role():
    dict_data = {
        "name": util.generate_fake_data("name"),
        "access_level": 10,
        "description": util.generate_fake_data("str"),
    }
    schema_data = schema.PostRole(**dict_data)
    role = models.Role(**schema_data.model_dump())
    role = role.create()
    yield role


def test_valid_data_and_meta():
    data = "test data"
    meta = {"key": "value"}
    response = Response(data, meta)
    assert response.data == data
    assert response.meta == meta


def test_valid_data_and_no_meta():
    data = "test data"
    response = Response(data)
    assert response.data == data
    assert response.meta == {}


def test_not_successful_create():
    with pytest.raises(HTTPException) as e:
        dict_data = {
            "nome_usuario": util.generate_fake_data("nome_usuario"),
            "email": util.generate_fake_data("email"),
            "senha": util.generate_fake_data("senha"),
            "active": util.generate_fake_data("bool"),
        }
        schema_data = schema.PostUser(**dict_data)
        user = models.Usuarios(**schema_data.model_dump())
        user.nome_usuario = None
        user.create()
    assert e.value.status_code == 555


def test_successful_login():
    user = models.Usuarios.login("nome_usuario", "admin", "admin")
    assert user is not None


def test_incorrect_password():
    with pytest.raises(HTTPException) as e:
        models.Usuarios.login("nome_usuario", "admin", "404")
    assert e.value.status_code == 401


def test_login_with_invalid_username():
    with pytest.raises(HTTPException) as e:
        models.Usuarios.login("nome_usuario", "404", "404")
    assert e.value.status_code == 404


def test_login_with_inactive_user(test_inactive_user):
    with pytest.raises(HTTPException) as e:
        models.Usuarios.login("nome_usuario", "nome_usuario", "senha")
    assert e.value.status_code == 401


def test_login_with_invalid_attribute():
    with pytest.raises(HTTPException) as e:
        models.Usuarios.login("not_username", "404", "404")
    assert e.value.status_code == 404


def test_include_query_params():
    user = models.Usuarios.query_params(
        all_data=True, include=["nome_usuario", "email"]
    )
    assert user is not None


def test_no_include_query_params():
    with pytest.raises(HTTPException) as e:
        data = models.Usuarios.query_params(all_data=True, include=["no_attr"])
    assert e.value.status_code == 404


def test_no_attribute_query_params():
    with pytest.raises(HTTPException) as e:
        data = models.Usuarios.query_params(all_data=True, attribute="no_attr")
    assert e.value.status_code == 404


def test_attribute_query_params():
    user = models.Usuarios.query_params(all_data=True, attribute="nome_usuario")
    assert user is not None


def test_equal_operator_query_params():
    data = models.Usuarios.query_params(
        all_data=True,
        attribute="nome_usuario",
        value="nome_usuario",
        operator="=",
    )
    assert data is not None


def test_alike_operator_query_params():
    data = models.Usuarios.query_params(
        all_data=True, attribute="nome_usuario", value="a", operator="~"
    )
    assert data is not None


def test_invalid_alike_operator_query_params():
    with pytest.raises(HTTPException) as e:
        data = models.Role.query_params(
            all_data=True,
            attribute="access_level",
            value="no_valid",
            operator="~",
        )
    assert e.value.status_code == 422


def test_dif_operator_query_params():
    data = models.Usuarios.query_params(
        all_data=True, attribute="nome_usuario", value="a", operator="!"
    )
    assert data is not None


def test_less_than_operator_query_params(test_base_role):
    data = models.Role.query_params(
        all_data=True, attribute="access_level", value="100", operator="<"
    )
    assert data is not None


def test_greater_than_operator_query_params():
    data = models.Role.query_params(
        all_data=True, attribute="access_level", value="1", operator=">"
    )
    assert data is not None


def test_invalid_value_greater_than_operator_query_params():
    with pytest.raises(HTTPException) as e:
        data = models.Role.query_params(
            all_data=True,
            attribute="access_level",
            value="no_valid",
            operator=">",
        )
    assert e.value.status_code == 422


def test_equal_greater_than_operator_query_params():
    data = models.Role.query_params(
        all_data=True, attribute="access_level", value="1", operator=">="
    )
    assert data is not None


def test_equal_less_than_operator_query_params():
    data = models.Role.query_params(
        all_data=True, attribute="access_level", value="1", operator="<="
    )
    assert data is not None


def test_or_operator_query_params():
    data = models.Role.query_params(
        all_data=True, attribute="access_level", value="1|90", operator="|"
    )
    assert data is not None


def test_invalid_or_operator_query_params():
    with pytest.raises(HTTPException) as e:
        data = models.Role.query_params(
            all_data=True,
            attribute="access_level",
            value="no_valid",
            operator="|",
        )
    assert e.value.status_code == 422


def test_invalid_operator_query_params():
    with pytest.raises(HTTPException) as e:
        data = models.Role.query_params(
            all_data=True,
            attribute="access_level",
            value="no_valid",
            operator="+",
        )
    assert e.value.status_code == 422


def test_json_string_operator_query_params():
    data = models.Role.query_params(all_data=True, json_string={"access_level": 1})
    assert data is not None


def test_invalid_formatted_json_string_query_params():
    with pytest.raises(HTTPException) as e:
        data = models.Role.query_params(all_data=True, json_string="no_valid")
    assert e.value.status_code == 422


def test_invalid_attribute_json_string_query_params():
    with pytest.raises(HTTPException) as e:
        data = models.Role.query_params(all_data=True, json_string={"no_valid": 1})
    assert e.value.status_code == 404


def test_remove_inactive_user(test_inactive_user):
    data = models.Usuarios.remove(test_inactive_user.id)
    assert data == "OK"
