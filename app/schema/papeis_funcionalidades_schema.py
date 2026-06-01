from datetime import datetime, date, time
from enum import Enum
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Form, Query
from pydantic import BaseModel, Field, ConfigDict, model_validator

from app.util import parse_operator_and_value
from app.core import ApiError

from .base_schema import *

from .funcionalidades_schema import GetFuncionalidades
from .papeis_schema import GetPapeis





__all__ = [
    "PostPapeisFuncionalidades",
    "GetPapeisFuncionalidades",
    "PatchPapeisFuncionalidades",
    "QueryPapeisFuncionalidadesDep",
]


class PostPapeisFuncionalidades(BaseModel):

    
    papel_id: UUID  = Field(..., description="Chave estrangeira referenciando o ID do Papeis")
    funcionalidade_id: UUID  = Field(..., description="")

    @model_validator(mode="before")
    @classmethod
    def validators_papeis_funcionalidades(self, data) -> "PostPapeisFuncionalidades":
        return data

    @classmethod
    def as_form(
        cls,
        papel_id: UUID = Form(..., description="Chave estrangeira referenciando o ID do Papeis"),
        funcionalidade_id: UUID = Form(..., description=""),
    ):
        return cls(
            papel_id=papel_id,
            funcionalidade_id=funcionalidade_id,
        )

class GetPapeisFuncionalidades(BaseModel):

    
    papel_id: UUID = Field(None, description="Chave estrangeira referenciando o ID do Papeis")
    funcionalidade_id: UUID = Field(None, description="")
    id: UUID = Field(None, description="Identificador único universal (UUIDv4) da entidade")
    criado_em: datetime = Field(None, description="Data e hora UTC da criação do registro")
    atualizado_em: datetime | None = Field(None, description="Data e hora UTC da última atualização do registro (null se nunca foi atualizado)")
    funcionalidades: GetFuncionalidades | None = Field(None)
    papeis: GetPapeis | None = Field(None)
    
    model_config = ConfigDict(from_attributes=True)


class PatchPapeisFuncionalidades(BaseModel):

    
    papel_id: UUID | None = Field(None, description="Chave estrangeira referenciando o ID do Papeis")
    funcionalidade_id: UUID | None = Field(None, description="")

class PapeisFuncionalidadesInclude(str, Enum):
    papel_id= "papel_id"
    funcionalidade_id= "funcionalidade_id"
    id= "id"
    criado_em= "criado_em"
    atualizado_em= "atualizado_em"

class PapeisFuncionalidadesExpand(str, Enum):
    funcionalidades = "funcionalidades"
    papeis = "papeis"

class SortOp(str, Enum):
    asc = "ASC"
    desc = "DESC"


class CursorDirection(str, Enum):
    next = "next"
    prev = "prev"

def get_expand_query():
    """Retorna a configuração apropriada para o campo expand."""
    members = list(PapeisFuncionalidadesExpand.__members__.values())

    # Se não há membros (nunca acontecerá com o template atual)
    if not members:
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Se o único membro é "Nenhum"
    if len(members) == 1 and hasattr(PapeisFuncionalidadesExpand, "Nenhum"):
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Caso contrário, retorna os valores válidos (excluindo "Nenhum" se existir)
    valid_expansions = [
        m.value for m in members
        if not (hasattr(PapeisFuncionalidadesExpand, "Nenhum") and m == PapeisFuncionalidadesExpand.Nenhum)
    ]

    return Query(
        None,
        description="Relacionamentos a expandir",
        include_in_schema=True
    )


class QueryPapeisFuncionalidades:
    def __init__(
        self,
        all_data: bool = Query(
            True,
            description="Retornar todas as correspondências ou apenas a primeira",
        ),
        # ==========================
        papel_id: str | None = Query(None, description="Chave estrangeira referenciando o ID do Papeis"),
        funcionalidade_id: str | None = Query(None, description=""),
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
        cursor_field: PapeisFuncionalidadesInclude = Query(
            PapeisFuncionalidadesInclude.id,
            description="Campo a ser usado como cursor (padrão: 'id')",
        ),
        cursor_direction: CursorDirection = Query(
            "next",
            description="Direção da paginação por cursor (next|prev)",
        ),
        # ==========================
        # Controle de retorno
        include: list[PapeisFuncionalidadesInclude] = Query(
            [], description="Atributos a incluir na resposta"
        ),
        exclude: list[PapeisFuncionalidadesInclude] = Query(
            [], description="Atributos a excluir da resposta"
        ),
        expand: list[PapeisFuncionalidadesExpand] | None = get_expand_query(),
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
        sort_field: PapeisFuncionalidadesInclude = Query(
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
        fields = [ f.value for f in PapeisFuncionalidadesInclude]
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


QueryPapeisFuncionalidadesDep = Annotated[QueryPapeisFuncionalidades, Depends()]