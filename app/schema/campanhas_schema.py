from datetime import datetime, date, time
from enum import Enum
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Form, Query
from pydantic import BaseModel, Field, ConfigDict, model_validator

from app.util import parse_operator_and_value
from app.core import ApiError

from .base_schema import *

from .enderecos_schema import GetEnderecos
from .campanhas_unidades_schema import GetCampanhasUnidades





__all__ = [
    "PostCampanhas",
    "GetCampanhas",
    "PatchCampanhas",
    "QueryCampanhasDep",
]


class PostCampanhas(BaseModel):

    
    nome: str  = Field(..., description="Nome da campanha")
    status: str  = Field(..., description="Status da campanha")
    doses_aplicadas: int  = Field(0,description="Quantidade de doses aplicadas na campanha")
    data_inicio: date  = Field(..., description="Data de início da campanha")
    data_fim: date  = Field(..., description="Data de fim da campanha")
    publico_alvo: str  = Field(..., description="Público-alvo da campanha")
    meta_vacinacao: int  = Field(..., description="Meta de vacinação da campanha")
    descricao: str  = Field(..., description="Descrição da campanha")
    horario_funcionamento: str  = Field(..., description="Horário de funcionamento da campanha")
    endereco_id: UUID  = Field(..., description="Chave estrangeira referenciando o Endereço")

    @model_validator(mode="before")
    @classmethod
    def validators_campanhas(self, data) -> "PostCampanhas":
        return data

    @classmethod
    def as_form(
        cls,
        nome: str = Form(..., description="Nome da campanha"),
        status: str = Form(..., description="Status da campanha"),
        doses_aplicadas: int = Form(..., description="Quantidade de doses aplicadas na campanha"),
        data_inicio: date = Form(..., description="Data de início da campanha"),
        data_fim: date = Form(..., description="Data de fim da campanha"),
        publico_alvo: str = Form(..., description="Público-alvo da campanha"),
        meta_vacinacao: int = Form(..., description="Meta de vacinação da campanha"),
        descricao: str = Form(..., description="Descrição da campanha"),
        horario_funcionamento: str = Form(..., description="Horário de funcionamento da campanha"),
        endereco_id: UUID = Form(..., description="Chave estrangeira referenciando o Endereço"),
    ):
        return cls(
            nome=nome,
            status=status,
            doses_aplicadas=doses_aplicadas,
            data_inicio=data_inicio,
            data_fim=data_fim,
            publico_alvo=publico_alvo,
            meta_vacinacao=meta_vacinacao,
            descricao=descricao,
            horario_funcionamento=horario_funcionamento,
            endereco_id=endereco_id,
        )

class GetCampanhas(BaseModel):

    
    nome: str = Field(None, description="Nome da campanha")
    status: str = Field(None, description="Status da campanha")
    doses_aplicadas: int = Field(None, description="Quantidade de doses aplicadas na campanha")
    data_inicio: date = Field(None, description="Data de início da campanha")
    data_fim: date = Field(None, description="Data de fim da campanha")
    publico_alvo: str = Field(None, description="Público-alvo da campanha")
    meta_vacinacao: int = Field(None, description="Meta de vacinação da campanha")
    descricao: str = Field(None, description="Descrição da campanha")
    horario_funcionamento: str = Field(None, description="Horário de funcionamento da campanha")
    endereco_id: UUID = Field(None, description="Chave estrangeira referenciando o Endereço")
    id: UUID = Field(None, description="Identificador único universal (UUIDv4) da entidade")
    criado_em: datetime = Field(None, description="Data e hora UTC da criação do registro")
    atualizado_em: datetime | None = Field(None, description="Data e hora UTC da última atualização do registro (null se nunca foi atualizado)")
    enderecos: GetEnderecos | None = Field(None)
    campanhas_unidades: list[GetCampanhasUnidades | None] = Field(None)
    
    model_config = ConfigDict(from_attributes=True)


class PatchCampanhas(BaseModel):

    
    nome: str | None = Field(None, description="Nome da campanha")
    status: str | None = Field(None, description="Status da campanha")
    doses_aplicadas: int | None = Field(None, description="Quantidade de doses aplicadas na campanha")
    data_inicio: date | None = Field(None, description="Data de início da campanha")
    data_fim: date | None = Field(None, description="Data de fim da campanha")
    publico_alvo: str | None = Field(None, description="Público-alvo da campanha")
    meta_vacinacao: int | None = Field(None, description="Meta de vacinação da campanha")
    descricao: str | None = Field(None, description="Descrição da campanha")
    horario_funcionamento: str | None = Field(None, description="Horário de funcionamento da campanha")
    endereco_id: UUID | None = Field(None, description="Chave estrangeira referenciando o Endereço")

class CampanhasInclude(str, Enum):
    nome= "nome"
    status= "status"
    doses_aplicadas= "doses_aplicadas"
    data_inicio= "data_inicio"
    data_fim= "data_fim"
    publico_alvo= "publico_alvo"
    meta_vacinacao= "meta_vacinacao"
    descricao= "descricao"
    horario_funcionamento= "horario_funcionamento"
    endereco_id= "endereco_id"
    id= "id"
    criado_em= "criado_em"
    atualizado_em= "atualizado_em"

class CampanhasExpand(str, Enum):
    enderecos = "enderecos"
    campanhas_unidades = "campanhas_unidades"

class SortOp(str, Enum):
    asc = "ASC"
    desc = "DESC"


class CursorDirection(str, Enum):
    next = "next"
    prev = "prev"

def get_expand_query():
    """Retorna a configuração apropriada para o campo expand."""
    members = list(CampanhasExpand.__members__.values())

    # Se não há membros (nunca acontecerá com o template atual)
    if not members:
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Se o único membro é "Nenhum"
    if len(members) == 1 and hasattr(CampanhasExpand, "Nenhum"):
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Caso contrário, retorna os valores válidos (excluindo "Nenhum" se existir)
    valid_expansions = [
        m.value for m in members
        if not (hasattr(CampanhasExpand, "Nenhum") and m == CampanhasExpand.Nenhum)
    ]

    return Query(
        None,
        description="Relacionamentos a expandir",
        include_in_schema=True
    )


class QueryCampanhas:
    def __init__(
        self,
        all_data: bool = Query(
            True,
            description="Retornar todas as correspondências ou apenas a primeira",
        ),
        # ==========================
        nome: str | None = Query(None, description="Nome da campanha"),
        status: str | None = Query(None, description="Status da campanha"),
        doses_aplicadas: str | None = Query(None, description="Quantidade de doses aplicadas na campanha"),
        data_inicio: str | None = Query(None, description="Data de início da campanha"),
        data_fim: str | None = Query(None, description="Data de fim da campanha"),
        publico_alvo: str | None = Query(None, description="Público-alvo da campanha"),
        meta_vacinacao: str | None = Query(None, description="Meta de vacinação da campanha"),
        descricao: str | None = Query(None, description="Descrição da campanha"),
        horario_funcionamento: str | None = Query(None, description="Horário de funcionamento da campanha"),
        endereco_id: str | None = Query(None, description="Chave estrangeira referenciando o Endereço"),
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
        cursor_field: CampanhasInclude = Query(
            CampanhasInclude.id,
            description="Campo a ser usado como cursor (padrão: 'id')",
        ),
        cursor_direction: CursorDirection = Query(
            "next",
            description="Direção da paginação por cursor (next|prev)",
        ),
        # ==========================
        # Controle de retorno
        include: list[CampanhasInclude] = Query(
            [], description="Atributos a incluir na resposta"
        ),
        exclude: list[CampanhasInclude] = Query(
            [], description="Atributos a excluir da resposta"
        ),
        expand: list[CampanhasExpand] | None = get_expand_query(),
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
        sort_field: CampanhasInclude = Query(
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
        fields = [ f.value for f in CampanhasInclude]
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


QueryCampanhasDep = Annotated[QueryCampanhas, Depends()]