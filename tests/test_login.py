from unittest import mock

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


from fastapi.security import OAuth2PasswordBearer


def test_login_access_token(test_client):
    response = test_client.post(
        "/api/v1/login/access-token",
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"nome_usuario": "admin", "senha": "admin"},
    )

    assert response.status_code == 200, f"Erro: {response.data}"

    json_response = response.json()
    assert "access_token" in json_response, "Token de acesso não encontrado na resposta"
    assert json_response["token_type"] == "Bearer", "Tipo de token incorreto"


def test_login_404(test_client):
    response = test_client.post(
        "/api/v1/login/access-token",
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"nome_usuario": "admin_", "senha": "admin_"},
    )

    assert response.status_code == 404, f"Erro: {response.data}"


# @mock.patch('app.util.send_email')
# @mock.patch('app.util.generate_code')
# @mock.patch('app.models.Usuarios.get')
# def test_forgot_my_password(mock_user_get, mock_generate_code, mock_send_email):
#     # Simula a função de gerar o código
#     mock_generate_code.return_value = "123456"

#     # Simula a existência de um usuário no banco de dados
#     mock_user_get.return_value = mock.Mock(uuid="123e4567-e89b-12d3-a456-426614174000")

#     # Define os dados de exemplo para a requisição
#     email_data = {
#         "email": "test@example.com"
#     }

#     # Realiza o POST para a rota de esqueci minha senha
#     response = client.post("/forgot-my-senha/", json=email_data)

#     # Verifica se o status da resposta é 200 (OK)
#     assert response.status_code == 200, f"Erro: {response.content}"

#     # Verifica se o código de redefinição de senha foi gerado e o e-mail foi enviado
#     mock_send_email.assert_called_once_with(
#         "test@example.com",
#         "SeuProjeto",  # Substitua pelo nome do seu projeto real
#         mock.ANY  # Não verificamos o conteúdo exato do e-mail aqui
#     )

#     # Verifica se o corpo da resposta contém o token
#     response_data = response.json()
#     assert "token" in response_data, "Token de reset não foi gerado"

#     # Verifica se o token foi codificado corretamente
#     assert isinstance(response_data["token"], str), "Token de reset deve ser uma string"
