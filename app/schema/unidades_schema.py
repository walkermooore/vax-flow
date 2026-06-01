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
from .agendas_schema import GetAgendas
from .lotes_schema import GetLotes
from .usuarios_schema import GetUsuarios
from .campanhas_unidades_schema import GetCampanhasUnidades





__all__ = [
    "PostUnidades",
    "GetUnidades",
    "PatchUnidades",
    "QueryUnidadesDep",
]


class PostUnidades(BaseModel):

    
    endereco_id: UUID | None  = Field(None, description="Chave estrangeira referenciando o Endereço")
    nome: str  = Field(..., description="Nome da unidade")
    nome_usuario_responsavel: str | None  = Field(None, description="Nome do usuário responsável pela unidade")
    tipo: str | None  = Field(None, description="Tipo da unidade")
    codigo_cnes: str  = Field(..., description="Código CNES da unidade")
    contato: str | None  = Field(None, description="Contato da unidade")
    email_unidade: str | None  = Field(None, description="E-mail da unidade")
    status: str | None  = Field(None, description="Status da unidade")
    capacidade_pacientes: str | None  = Field(None, description="Capacidade de pacientes da unidade")
    horario_funcionamento: str | None  = Field(None, description="Horário de funcionamento da unidade")
    informacoes_servico: str | None  = Field(None, description="Informações sobre os serviços da unidade")

    @model_validator(mode="before")
    @classmethod
    def validators_unidades(self, data) -> "PostUnidades":
        if not "codigo_cnes" in data:
            raise ValueError("É necessário informar o codigo_cnes para prosseguir.")
        return data

    @classmethod
    def as_form(
        cls,
        endereco_id: UUID | None = Form(None, description="Chave estrangeira referenciando o Endereço"),
        nome: str = Form(..., description="Nome da unidade"),
        nome_usuario_responsavel: str | None = Form(None, description="Nome do usuário responsável pela unidade"),
        tipo: str | None = Form(None, description="Tipo da unidade"),
        codigo_cnes: str = Form(..., description="Código CNES da unidade"),
        contato: str | None = Form(None, description="Contato da unidade"),
        email_unidade: str | None = Form(None, description="E-mail da unidade"),
        status: str | None = Form(None, description="Status da unidade"),
        capacidade_pacientes: str | None = Form(None, description="Capacidade de pacientes da unidade"),
        horario_funcionamento: str | None = Form(None, description="Horário de funcionamento da unidade"),
        informacoes_servico: str | None = Form(None, description="Informações sobre os serviços da unidade"),
    ):
        return cls(
            endereco_id=endereco_id,
            nome=nome,
            nome_usuario_responsavel=nome_usuario_responsavel,
            tipo=tipo,
            codigo_cnes=codigo_cnes,
            contato=contato,
            email_unidade=email_unidade,
            status=status,
            capacidade_pacientes=capacidade_pacientes,
            horario_funcionamento=horario_funcionamento,
            informacoes_servico=informacoes_servico,
        )

class GetUnidades(BaseModel):

    
    endereco_id: UUID | None = Field(None, description="Chave estrangeira referenciando o Endereço")
    nome: str = Field(None, description="Nome da unidade")
    nome_usuario_responsavel: str | None = Field(None, description="Nome do usuário responsável pela unidade")
    tipo: str | None = Field(None, description="Tipo da unidade")
    codigo_cnes: str = Field(None, description="Código CNES da unidade")
    contato: str | None = Field(None, description="Contato da unidade")
    email_unidade: str | None = Field(None, description="E-mail da unidade")
    status: str | None = Field(None, description="Status da unidade")
    capacidade_pacientes: str | None = Field(None, description="Capacidade de pacientes da unidade")
    horario_funcionamento: str | None = Field(None, description="Horário de funcionamento da unidade")
    informacoes_servico: str | None = Field(None, description="Informações sobre os serviços da unidade")
    id: UUID = Field(None, description="Identificador único universal (UUIDv4) da entidade")
    criado_em: datetime = Field(None, description="Data e hora UTC da criação do registro")
    atualizado_em: datetime | None = Field(None, description="Data e hora UTC da última atualização do registro (null se nunca foi atualizado)")
    enderecos: GetEnderecos | None = Field(None)
    agendas: list[GetAgendas | None] = Field(None)
    lotes: list[GetLotes | None] = Field(None)
    usuarios: list[GetUsuarios | None] = Field(None)
    campanhas_unidades: list[GetCampanhasUnidades | None] = Field(None)
    
    model_config = ConfigDict(from_attributes=True)


class PatchUnidades(BaseModel):

    
    endereco_id: UUID | None = Field(None, description="Chave estrangeira referenciando o Endereço")
    nome: str | None = Field(None, description="Nome da unidade")
    nome_usuario_responsavel: str | None = Field(None, description="Nome do usuário responsável pela unidade")
    tipo: str | None = Field(None, description="Tipo da unidade")
    codigo_cnes: str | None = Field(None, description="Código CNES da unidade")
    contato: str | None = Field(None, description="Contato da unidade")
    email_unidade: str | None = Field(None, description="E-mail da unidade")
    status: str | None = Field(None, description="Status da unidade")
    capacidade_pacientes: str | None = Field(None, description="Capacidade de pacientes da unidade")
    horario_funcionamento: str | None = Field(None, description="Horário de funcionamento da unidade")
    informacoes_servico: str | None = Field(None, description="Informações sobre os serviços da unidade")

class UnidadesInclude(str, Enum):
    endereco_id= "endereco_id"
    nome= "nome"
    nome_usuario_responsavel= "nome_usuario_responsavel"
    tipo= "tipo"
    codigo_cnes= "codigo_cnes"
    contato= "contato"
    email_unidade= "email_unidade"
    status= "status"
    capacidade_pacientes= "capacidade_pacientes"
    horario_funcionamento= "horario_funcionamento"
    informacoes_servico= "informacoes_servico"
    id= "id"
    criado_em= "criado_em"
    atualizado_em= "atualizado_em"

class UnidadesExpand(str, Enum):
    enderecos = "enderecos"
    agendas = "agendas"
    lotes = "lotes"
    usuarios = "usuarios"
    campanhas_unidades = "campanhas_unidades"

class SortOp(str, Enum):
    asc = "ASC"
    desc = "DESC"


class CursorDirection(str, Enum):
    next = "next"
    prev = "prev"

def get_expand_query():
    """Retorna a configuração apropriada para o campo expand."""
    members = list(UnidadesExpand.__members__.values())

    # Se não há membros (nunca acontecerá com o template atual)
    if not members:
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Se o único membro é "Nenhum"
    if len(members) == 1 and hasattr(UnidadesExpand, "Nenhum"):
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Caso contrário, retorna os valores válidos (excluindo "Nenhum" se existir)
    valid_expansions = [
        m.value for m in members
        if not (hasattr(UnidadesExpand, "Nenhum") and m == UnidadesExpand.Nenhum)
    ]

    return Query(
        None,
        description="Relacionamentos a expandir",
        include_in_schema=True
    )


class QueryUnidades:
    def __init__(
        self,
        all_data: bool = Query(
            True,
            description="Retornar todas as correspondências ou apenas a primeira",
        ),
        # ==========================
        endereco_id: str | None = Query(None, description="Chave estrangeira referenciando o Endereço"),
        nome: str | None = Query(None, description="Nome da unidade"),
        nome_usuario_responsavel: str | None = Query(None, description="Nome do usuário responsável pela unidade"),
        tipo: str | None = Query(None, description="Tipo da unidade"),
        codigo_cnes: str | None = Query(None, description="Código CNES da unidade"),
        contato: str | None = Query(None, description="Contato da unidade"),
        email_unidade: str | None = Query(None, description="E-mail da unidade"),
        status: str | None = Query(None, description="Status da unidade"),
        capacidade_pacientes: str | None = Query(None, description="Capacidade de pacientes da unidade"),
        horario_funcionamento: str | None = Query(None, description="Horário de funcionamento da unidade"),
        informacoes_servico: str | None = Query(None, description="Informações sobre os serviços da unidade"),
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
        cursor_field: UnidadesInclude = Query(
            UnidadesInclude.id,
            description="Campo a ser usado como cursor (padrão: 'id')",
        ),
        cursor_direction: CursorDirection = Query(
            "next",
            description="Direção da paginação por cursor (next|prev)",
        ),
        # ==========================
        # Controle de retorno
        include: list[UnidadesInclude] = Query(
            [], description="Atributos a incluir na resposta"
        ),
        exclude: list[UnidadesInclude] = Query(
            [], description="Atributos a excluir da resposta"
        ),
        expand: list[UnidadesExpand] | None = get_expand_query(),
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
        sort_field: UnidadesInclude = Query(
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
        fields = [ f.value for f in UnidadesInclude]
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


QueryUnidadesDep = Annotated[QueryUnidades, Depends()]