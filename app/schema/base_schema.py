from typing import Annotated

from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator, BeforeValidator

from app.util.validators import (normalize_email, normalize_lower,
                                 normalize_password, validate_cnpj,
                                 validate_cnpj_cpf, validate_cpf, validate_uf)

__all__ = [
    "Senha",
    "NomeUsuario",
    "Email",
    "UF",
    "Cpf",
    "Cnpj",
    "CpfCnpj",
    "MetaData",
]


class MetaData(BaseModel):
    total_data: int
    query_items: int


Senha = Annotated[bytes, AfterValidator(normalize_password)]
NomeUsuario = Annotated[str, AfterValidator(normalize_lower)]
UF = Annotated[str, AfterValidator(validate_uf)]
Email = Annotated[str, BeforeValidator(normalize_email)]
Cpf = Annotated[str, AfterValidator(validate_cpf)]
Cnpj = Annotated[str, AfterValidator(validate_cnpj)]
CpfCnpj = Annotated[str, AfterValidator(validate_cnpj_cpf)]
