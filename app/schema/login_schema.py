from fastapi import Form
from pydantic import BaseModel, ConfigDict, Field

from .base_schema import NomeUsuario, Senha
from .usuarios_schema import GetUsuarios

# from .user_schema import GetUser


__all__ = [
    "Login",
    "ResponseLoginAcessToken",
    "EsqueciSenha",
    "ResponseEsqueciSenha",
    "ResponseLoginSessionToken",
    "NovaSenha",
    "ResponseEsqueciSenhaCodigo",
]


class Login(BaseModel):
    """Schema utilizado no Login

    Attributes:
        nome_usuario (str): Nome do Usuarios.
        senha(str): Senha.
    """

    username: str = Field(..., description="nome_usuario Documentar")
    password: str = Field(..., description="senha Documentar")

    @classmethod
    def as_form(
        cls,
        username: NomeUsuario = Form(..., description="nome_usuario Documentar"),
        password: str = Form(..., description="senha Documentar"),
    ):
        return cls(
            username=username,
            password=password,
        )


class ResponseLoginAcessToken(BaseModel):
    access_token: str
    token_type: str
    permission: list[str] | None
    user: GetUsuarios
    papel: str

    model_config = ConfigDict(from_attributes=True)


class ResponseLoginSessionToken(BaseModel):
    user: GetUsuarios

    model_config = ConfigDict(from_attributes=True)


class EsqueciSenha(BaseModel):
    email: str


class ResponseEsqueciSenha(BaseModel):
    token: str
    model_config = ConfigDict(from_attributes=True)


class ResponseEsqueciSenhaCodigo(BaseModel):
    token: str
    model_config = ConfigDict(from_attributes=True)


class NovaSenha(BaseModel):
    senha: Senha = Form(description="Senha")
