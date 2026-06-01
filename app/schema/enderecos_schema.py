from datetime import datetime, date, time
from enum import Enum
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Form, Query
from pydantic import BaseModel, Field, ConfigDict, model_validator

from app.util import parse_operator_and_value
from app.core import ApiError

from .base_schema import *






__all__ = [
    "PostEnderecos",
    "GetEnderecos",
    "PatchEnderecos",
    "QueryEnderecosDep",
]


class PostEnderecos(BaseModel):

    
    nomeLocal: str  = Field(..., description="Nome do local")
    logradouro: str  = Field(..., description="Logradouro do endereço")
    numero: str  = Field(..., description="Número do endereço")
    complemento: str | None  = Field(None, description="Complemento do endereço")
    bairro: str  = Field(..., description="Bairro do endereço")
    cep: str  = Field(..., description="CEP do endereço")
    cidade: str  = Field(..., description="Cidade do endereço")
    estado: str  = Field(..., description="Estado do endereço")
    latitude: float  = Field(..., description="Latitude geográfica")
    longitude: float  = Field(..., description="Longitude geográfica")

    @model_validator(mode="before")
    @classmethod
    def validators_enderecos(self, data) -> "PostEnderecos":
        return data

    @classmethod
    def as_form(
        cls,
        nomeLocal: str = Form(..., description="Nome do local"),
        logradouro: str = Form(..., description="Logradouro do endereço"),
        numero: str = Form(..., description="Número do endereço"),
        complemento: str | None = Form(None, description="Complemento do endereço"),
        bairro: str = Form(..., description="Bairro do endereço"),
        cep: str = Form(..., description="CEP do endereço"),
        cidade: str = Form(..., description="Cidade do endereço"),
        estado: str = Form(..., description="Estado do endereço"),
        latitude: float = Form(..., description="Latitude geográfica"),
        longitude: float = Form(..., description="Longitude geográfica"),
    ):
        return cls(
            nomeLocal=nomeLocal,
            logradouro=logradouro,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cep=cep,
            cidade=cidade,
            estado=estado,
            latitude=latitude,
            longitude=longitude,
        )

class GetEnderecos(BaseModel):

    
    nomeLocal: str = Field(None, description="Nome do local")
    logradouro: str = Field(None, description="Logradouro do endereço")
    numero: str = Field(None, description="Número do endereço")
    complemento: str | None = Field(None, description="Complemento do endereço")
    bairro: str = Field(None, description="Bairro do endereço")
    cep: str = Field(None, description="CEP do endereço")
    cidade: str = Field(None, description="Cidade do endereço")
    estado: str = Field(None, description="Estado do endereço")
    latitude: float = Field(None, description="Latitude geográfica")
    longitude: float = Field(None, description="Longitude geográfica")
    id: UUID = Field(None, description="Identificador único universal (UUIDv4) da entidade")
    criado_em: datetime = Field(None, description="Data e hora UTC da criação do registro")
    atualizado_em: datetime | None = Field(None, description="Data e hora UTC da última atualização do registro (null se nunca foi atualizado)")
    
    model_config = ConfigDict(from_attributes=True)


class PatchEnderecos(BaseModel):

    
    nomeLocal: str | None = Field(None, description="Nome do local")
    logradouro: str | None = Field(None, description="Logradouro do endereço")
    numero: str | None = Field(None, description="Número do endereço")
    complemento: str | None = Field(None, description="Complemento do endereço")
    bairro: str | None = Field(None, description="Bairro do endereço")
    cep: str | None = Field(None, description="CEP do endereço")
    cidade: str | None = Field(None, description="Cidade do endereço")
    estado: str | None = Field(None, description="Estado do endereço")
    latitude: float | None = Field(None, description="Latitude geográfica")
    longitude: float | None = Field(None, description="Longitude geográfica")

class EnderecosInclude(str, Enum):
    nomeLocal= "nomeLocal"
    logradouro= "logradouro"
    numero= "numero"
    complemento= "complemento"
    bairro= "bairro"
    cep= "cep"
    cidade= "cidade"
    estado= "estado"
    latitude= "latitude"
    longitude= "longitude"
    id= "id"
    criado_em= "criado_em"
    atualizado_em= "atualizado_em"

class EnderecosExpand(str, Enum):
    Nenhum = ""

class SortOp(str, Enum):
    asc = "ASC"
    desc = "DESC"


class CursorDirection(str, Enum):
    next = "next"
    prev = "prev"

def get_expand_query():
    """Retorna a configuração apropriada para o campo expand."""
    members = list(EnderecosExpand.__members__.values())

    # Se não há membros (nunca acontecerá com o template atual)
    if not members:
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Se o único membro é "Nenhum"
    if len(members) == 1 and hasattr(EnderecosExpand, "Nenhum"):
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Caso contrário, retorna os valores válidos (excluindo "Nenhum" se existir)
    valid_expansions = [
        m.value for m in members
        if not (hasattr(EnderecosExpand, "Nenhum") and m == EnderecosExpand.Nenhum)
    ]

    return Query(
        None,
        description="Relacionamentos a expandir",
        include_in_schema=True
    )


class QueryEnderecos:
    def __init__(
        self,
        all_data: bool = Query(
            True,
            description="Retornar todas as correspondências ou apenas a primeira",
        ),
        # ==========================
        nomeLocal: str | None = Query(None, description="Nome do local"),
        logradouro: str | None = Query(None, description="Logradouro do endereço"),
        numero: str | None = Query(None, description="Número do endereço"),
        complemento: str | None = Query(None, description="Complemento do endereço"),
        bairro: str | None = Query(None, description="Bairro do endereço"),
        cep: str | None = Query(None, description="CEP do endereço"),
        cidade: str | None = Query(None, description="Cidade do endereço"),
        estado: str | None = Query(None, description="Estado do endereço"),
        latitude: str | None = Query(None, description="Latitude geográfica"),
        longitude: str | None = Query(None, description="Longitude geográfica"),
        id: str | None = Query(None, description="Identificador único universal (UUIDv4) da entidade"),
        criado_em: str | None = Query(None, description="Data e hora UTC da criação do registro"),
        atualizado_em: str | None = Query(None, description="Data e hora UTC da última atualização do registro (null se nunca foi atualizado)"),
        # ==========================
        # Paginação numérica
        limit: int | None = Query(
            None, description="Número máximo de itens a retornar"
        ),
        offset: int | None = Query(
            None, description="Offset absoluto para paginação (alternativa a skip)"
        ),
        # ==========================
        # Paginação por cursor
        cursor: str | None = Query(
            None, description="Valor do cursor para paginação baseada em cursor"
        ),
        cursor_field: EnderecosInclude = Query(
            EnderecosInclude.id,
            description="Campo a ser usado como cursor (padrão: 'id')",
        ),
        cursor_direction: CursorDirection = Query(
            "next",
            description="Direção da paginação por cursor (next|prev)",
        ),
        # ==========================
        # Controle de retorno
        include: list[EnderecosInclude] = Query(
            [], description="Atributos a incluir na resposta"
        ),
        exclude: list[EnderecosInclude] = Query(
            [], description="Atributos a excluir da resposta"
        ),
        expand: list[EnderecosExpand] | None = get_expand_query(),
        count_only: bool = Query(
            False,
            description="Retornar apenas a contagem total de itens, sem os dados",
        ),
        distinct: bool = Query(
            False,
            description="Aplicar DISTINCT na consulta para evitar duplicatas",
        ),
        # ==========================
        # Ordenação
        sort_op: SortOp = Query(
            None, description="operador da ordem do resultado (ASC | DESC)"
        ),
        sort_field: EnderecosInclude = Query(
            None, description="ordem do resultado (ex: criado_em)"
        ),
    ):
        self.all_data = all_data
        self.count_only = count_only
        self.distinct = distinct

        # Paginação
        self.limit = limit
        self.offset = offset
        self.cursor = cursor
        self.cursor_field = cursor_field.value if cursor_field else "id"
        self.cursor_direction = cursor_direction.value if cursor_direction else "next"

        # Seleção de campos
        self.include = [name.value for name in include]
        self.exclude = [name.value for name in exclude]
        self.expand = expand

        # Ordenação
        self.sort_op = sort_op.value if sort_op else None
        self.sort_field = sort_field.value if sort_field else None

        # Construção dos filtros
        self.filters = {}
        fields = [ f.value for f in EnderecosInclude]
        for field in fields:
            value = locals()[field]
            if value:
                self.filters[field] = parse_operator_and_value(value)

        # Validações
        if not all_data and not self.filters:
            raise ApiError(
                status_code=400,
                msg="Quando a consulta não é de todas as correspondências, filtros ou busca textual são obrigatórios",
            )

        if cursor and not cursor_field:
            raise ApiError(
                status_code=400,
                msg="Campo do cursor é obrigatório quando usando paginação por cursor",
            )


QueryEnderecosDep = Annotated[QueryEnderecos, Depends()]