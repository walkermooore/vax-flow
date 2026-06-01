import datetime
import json
import logging
from typing import Optional, Union

import jwt
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer

from app import core, models
from app.core import ApiError
from app.db.session import SessionLocal
from app.models import Funcionalidades, Usuarios

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/access-token")


__all__ = ["Key", "encode_token", "decode_token", "Session"]


def encode_token(sub, exp):
    """
    Codifica um token JWT.

    Args:
        sub (Any): O assunto do token.
        exp (Union[int, float]): O tempo de expiração do token em minutos.

    Returns:
        str: O token JWT codificado.
    """

    payload = {
        "exp": datetime.datetime.now(tz=datetime.timezone.utc)
        + datetime.timedelta(minutes=exp),
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "sub": sub,
    }
    result = jwt.encode(payload, core.settings.SECRET_KEY, algorithm="HS256")
    return result


def get_user_from_payload(sub: dict) -> Usuarios:
    user_id = sub["user_id"]
    if not user_id:
        raise ApiError(
            status_code=403,
            loc=["body"],
            msg=f"Desculpe, você não tem permissão.",
            type="value_error.auth",
        )
    user = Usuarios.get("id", user_id)
    if not user:
        raise ApiError(
            status_code=401,
            loc=["body"],
            msg=f"Desculpe, usuário não encontrado.",
            type="value_error.auth",
        )
    if not user.active:
        raise ApiError(
            status_code=401,
            loc=["body"],
            msg=f"Desculpe, usuário desativado ou excluído.",
            type="value_error.auth",
        )
    return user

def remover_ultima_parte(path):
    """
    Remove a última parte do path se não terminar com /
    Exemplo: '/usuarios/142d56a4-25a6-46e6-b99f-05e11e5a906a' → '/usuarios/'
    """
    if path.endswith('/'):
        return path
    
    # Encontra a última barra
    ultima_barra = path.rfind('/')
    if ultima_barra != -1:
        return path[:ultima_barra + 1]
    
    return path + '/'

def url_key(path, method):
    session = SessionLocal()
    try:
        path = remover_ultima_parte(path)
        functionality_data = Funcionalidades.query_params(
            session,
            all_data=True,
            filters={"caminho": path, "metodo": method},
        ).data

        if functionality_data:
            return functionality_data[0].chave
        else:
            return 0
    finally:
        session.close()


def decode_token(token: str, key: Union[int, None] = None) -> dict:
    try:
        payload = jwt.decode(token, core.settings.SECRET_KEY, algorithms="HS256")
        if type(payload["sub"]) == str:
            sub = json.loads(payload["sub"])
        else:
            sub = payload["sub"]
    except jwt.ExpiredSignatureError:
        raise ApiError(
            status_code=401,
            loc=["body"],
            msg=f"Desculpe, o token expirou.",
            type="value_error.auth",
        )
    except jwt.InvalidTokenError:
        raise ApiError(
            status_code=401,
            loc=["body"],
            msg=f"Desculpe, o token é inválido.",
            type="value_error.auth",
        )
    if "user_id" in sub:
        user = get_user_from_payload(sub)
    if key and key not in sub["chave"]:
        raise ApiError(
            status_code=403,
            loc=["body"],
            msg=f"Desculpe, você não tem permissão.",
            type="value_error.auth",
        )

    return sub


class Key:
    async def closed(
        request: Request,
        token: str = Depends(oauth2_scheme),
    ):

        key = url_key(request.scope["path"], request.scope["method"])
        print(key)
        payload = decode_token(token, key)
        return payload

    async def open():
        return


# para utilizar session deve-se descomentar a liha do session midleware em app/main e adicionar a lib 'itsdangerous'
class Session:
    async def closed(request: Request):
        key = url_key(request.scope["path"], request.scope["method"])
        token = request.session.get("token")
        payload = decode_token(token, key)
        return payload

    async def open():
        return
