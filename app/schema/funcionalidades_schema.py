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
    "PostFuncionalidades",
    "GetFuncionalidades",
    "PatchFuncionalidades",
    "QueryFuncionalidadesDep",
]


class PostFuncionalidades(BaseModel):

    
    nome: str  = Field(..., description="Nome amigável da funcionalidades (ex: 'Excluir Cliente')")
    escopo: str  = Field(..., description="Identificador único no formato 'recurso:ação' (ex: 'client:delete')")
    caminho: str  = Field(..., description="Endpoint da API (ex: '/api/client/{id}')")
    metodo: str  = Field(..., description="Método HTTP (GET, POST, PUT, DELETE, etc)")
    descricao: str | None  = Field(None, description="Descrição detalhada do propósito da funcionalidades")
    categoria: str | None  = Field(None, description="Grupo funcional (ex: 'CRM', 'Financeiro', 'Relatórios')")
    sensivel: bool | None  = Field(False,description="Indica se é uma operação crítica/cuidado extra necessário")
    versao: int | None  = Field(1,description="Versão da funcionalidades para controle de evolução")

    @model_validator(mode="before")
    @classmethod
    def validators_funcionalidades(self, data) -> "PostFuncionalidades":
        if not "escopo" in data:
            raise ValueError("É necessário informar o escopo para prosseguir.")
        return data

    @classmethod
    def as_form(
        cls,
        nome: str = Form(..., description="Nome amigável da funcionalidades (ex: 'Excluir Cliente')"),
        escopo: str = Form(..., description="Identificador único no formato 'recurso:ação' (ex: 'client:delete')"),
        caminho: str = Form(..., description="Endpoint da API (ex: '/api/client/{id}')"),
        metodo: str = Form(..., description="Método HTTP (GET, POST, PUT, DELETE, etc)"),
        descricao: str | None = Form(None, description="Descrição detalhada do propósito da funcionalidades"),
        categoria: str | None = Form(None, description="Grupo funcional (ex: 'CRM', 'Financeiro', 'Relatórios')"),
        sensivel: bool | None = Form(None, description="Indica se é uma operação crítica/cuidado extra necessário"),
        versao: int | None = Form(None, description="Versão da funcionalidades para controle de evolução"),
    ):
        return cls(
            nome=nome,
            escopo=escopo,
            caminho=caminho,
            metodo=metodo,
            descricao=descricao,
            categoria=categoria,
            sensivel=sensivel,
            versao=versao,
        )

class GetFuncionalidades(BaseModel):

    
    chave: int | None = Field(None, description="Chave de acesso autoincrementada")
    nome: str = Field(None, description="Nome amigável da funcionalidades (ex: 'Excluir Cliente')")
    escopo: str = Field(None, description="Identificador único no formato 'recurso:ação' (ex: 'client:delete')")
    caminho: str = Field(None, description="Endpoint da API (ex: '/api/client/{id}')")
    metodo: str = Field(None, description="Método HTTP (GET, POST, PUT, DELETE, etc)")
    descricao: str | None = Field(None, description="Descrição detalhada do propósito da funcionalidades")
    categoria: str | None = Field(None, description="Grupo funcional (ex: 'CRM', 'Financeiro', 'Relatórios')")
    sensivel: bool | None = Field(None, description="Indica se é uma operação crítica/cuidado extra necessário")
    versao: int | None = Field(None, description="Versão da funcionalidades para controle de evolução")
    id: UUID = Field(None, description="Identificador único universal (UUIDv4) da entidade")
    criado_em: datetime = Field(None, description="Data e hora UTC da criação do registro")
    atualizado_em: datetime | None = Field(None, description="Data e hora UTC da última atualização do registro (null se nunca foi atualizado)")
    
    model_config = ConfigDict(from_attributes=True)


class PatchFuncionalidades(BaseModel):

    
    nome: str | None = Field(None, description="Nome amigável da funcionalidades (ex: 'Excluir Cliente')")
    escopo: str | None = Field(None, description="Identificador único no formato 'recurso:ação' (ex: 'client:delete')")
    caminho: str | None = Field(None, description="Endpoint da API (ex: '/api/client/{id}')")
    metodo: str | None = Field(None, description="Método HTTP (GET, POST, PUT, DELETE, etc)")
    descricao: str | None = Field(None, description="Descrição detalhada do propósito da funcionalidades")
    categoria: str | None = Field(None, description="Grupo funcional (ex: 'CRM', 'Financeiro', 'Relatórios')")
    sensivel: bool | None = Field(None, description="Indica se é uma operação crítica/cuidado extra necessário")
    versao: int | None = Field(None, description="Versão da funcionalidades para controle de evolução")

class FuncionalidadesInclude(str, Enum):
    chave= "chave"
    nome= "nome"
    escopo= "escopo"
    caminho= "caminho"
    metodo= "metodo"
    descricao= "descricao"
    categoria= "categoria"
    sensivel= "sensivel"
    versao= "versao"
    id= "id"
    criado_em= "criado_em"
    atualizado_em= "atualizado_em"

class FuncionalidadesExpand(str, Enum):
    Nenhum = ""

class SortOp(str, Enum):
    asc = "ASC"
    desc = "DESC"


class CursorDirection(str, Enum):
    next = "next"
    prev = "prev"

def get_expand_query():
    """Retorna a configuração apropriada para o campo expand."""
    members = list(FuncionalidadesExpand.__members__.values())

    # Se não há membros (nunca acontecerá com o template atual)
    if not members:
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Se o único membro é "Nenhum"
    if len(members) == 1 and hasattr(FuncionalidadesExpand, "Nenhum"):
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Caso contrário, retorna os valores válidos (excluindo "Nenhum" se existir)
    valid_expansions = [
        m.value for m in members
        if not (hasattr(FuncionalidadesExpand, "Nenhum") and m == FuncionalidadesExpand.Nenhum)
    ]

    return Query(
        None,
        description="Relacionamentos a expandir",
        include_in_schema=True
    )


class QueryFuncionalidades:
    def __init__(
        self,
        all_data: bool = Query(
            True,
            description="Retornar todas as correspondências ou apenas a primeira",
        ),
        # ==========================
        chave: str | None = Query(None, description="Chave de acesso autoincrementada"),
        nome: str | None = Query(None, description="Nome amigável da funcionalidades (ex: 'Excluir Cliente')"),
        escopo: str | None = Query(None, description="Identificador único no formato 'recurso:ação' (ex: 'client:delete')"),
        caminho: str | None = Query(None, description="Endpoint da API (ex: '/api/client/{id}')"),
        metodo: str | None = Query(None, description="Método HTTP (GET, POST, PUT, DELETE, etc)"),
        descricao: str | None = Query(None, description="Descrição detalhada do propósito da funcionalidades"),
        categoria: str | None = Query(None, description="Grupo funcional (ex: 'CRM', 'Financeiro', 'Relatórios')"),
        sensivel: str | None = Query(None, description="Indica se é uma operação crítica/cuidado extra necessário"),
        versao: str | None = Query(None, description="Versão da funcionalidades para controle de evolução"),
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
        cursor_field: FuncionalidadesInclude = Query(
            FuncionalidadesInclude.id,
            description="Campo a ser usado como cursor (padrão: 'id')",
        ),
        cursor_direction: CursorDirection = Query(
            "next",
            description="Direção da paginação por cursor (next|prev)",
        ),
        # ==========================
        # Controle de retorno
        include: list[FuncionalidadesInclude] = Query(
            [], description="Atributos a incluir na resposta"
        ),
        exclude: list[FuncionalidadesInclude] = Query(
            [], description="Atributos a excluir da resposta"
        ),
        expand: list[FuncionalidadesExpand] | None = get_expand_query(),
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
        sort_field: FuncionalidadesInclude = Query(
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
        fields = [ f.value for f in FuncionalidadesInclude]
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


QueryFuncionalidadesDep = Annotated[QueryFuncionalidades, Depends()]