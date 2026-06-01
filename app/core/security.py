import logging

import bcrypt

from .responses import ApiError

__all__ = ["get_password_hash", "verify_password"]


def verify_password(plain_password: str | bytes, hashed_password: str | bytes) -> bool:
    try:
        if str(type(plain_password)) != "<class 'bytes'>":
            plain_password = plain_password.encode()
        if str(type(hashed_password)) != "<class 'bytes'>":
            hashed_password = hashed_password.encode()
        return bcrypt.checkpw(plain_password, hashed_password)
    except Exception as e:
        logging.warning(e) if not hasattr(e, "status_code") else ...
        raise ApiError(
            status_code=404,
            loc=["body", "senha"],
            msg=f"Erro de Autenticação",
            type="value_error.core.security",
        )


def get_password_hash(senha: str | bytes) -> bytes:
    try:
        if str(type(senha)) != "<class 'bytes'>":
            senha = senha.encode()
        return bcrypt.hashpw(senha, bcrypt.gensalt())
    except Exception as e:
        logging.warning(e) if not hasattr(e, "status_code") else ...
        raise ApiError(
            status_code=404,
            loc=["body", "senha"],
            msg=f"Erro de Autenticação",
            type="value_error.core.security",
        )
