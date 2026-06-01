from datetime import datetime, date, time
from enum import Enum
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Form, Query
from pydantic import BaseModel, Field, ConfigDict, model_validator

from app.util import parse_operator_and_value
from app.core import ApiError

from .base_schema import *

from .usuarios_schema import GetUsuarios
from .vacinas_aplicadas_schema import GetVacinasAplicadas





__all__ = [
    "PostAgendamentos",
    "GetAgendamentos",
    "PatchAgendamentos",
    "QueryAgendamentosDep",
]


class PostAgendamentos(BaseModel):

    
    agenda_id: UUID  = Field(..., description="Chave estrangeira referenciando a Agenda")
    vacina: str | None  = Field(None, description="Nome da vacina a ser aplicada")
    tipo_identificacao_paciente: str  = Field(..., description="Tipo de identificação do paciente")
    numero_identificacao_paciente: str  = Field(..., description="Número de identificação do paciente")
    hora: time  = Field(..., description="Hora do agendamento")
    data: date  = Field(..., description="Data do agendamento")
    protocolo: str | None  = Field(None, description="Protocolo do agendamento")
    status: str | None  = Field(None, description="Status do agendamento")
    registro_data_hora_atendimento: datetime | None  = Field(None, description="Data e hora do atendimento registrado")
    usuario_responsavel_id: UUID | None  = Field(None, description="Chave estrangeira referenciando o Usuário Responsável")
    usuario_responsavel_nome: str | None  = Field(None, description="Nome do usuário responsável pelo atendimento")

    @model_validator(mode="before")
    @classmethod
    def validators_agendamentos(self, data) -> "PostAgendamentos":
        if not "protocolo" in data:
            raise ValueError("É necessário informar o protocolo para prosseguir.")
        return data

    @classmethod
    def as_form(
        cls,
        agenda_id: UUID = Form(..., description="Chave estrangeira referenciando a Agenda"),
        vacina: str | None = Form(None, description="Nome da vacina a ser aplicada"),
        tipo_identificacao_paciente: str = Form(..., description="Tipo de identificação do paciente"),
        numero_identificacao_paciente: str = Form(..., description="Número de identificação do paciente"),
        hora: time = Form(..., description="Hora do agendamento"),
        data: date = Form(..., description="Data do agendamento"),
        protocolo: str | None = Form(None, description="Protocolo do agendamento"),
        status: str | None = Form(None, description="Status do agendamento"),
        registro_data_hora_atendimento: datetime | None = Form(None, description="Data e hora do atendimento registrado"),
        usuario_responsavel_id: UUID | None = Form(None, description="Chave estrangeira referenciando o Usuário Responsável"),
        usuario_responsavel_nome: str | None = Form(None, description="Nome do usuário responsável pelo atendimento"),
    ):
        return cls(
            agenda_id=agenda_id,
            vacina=vacina,
            tipo_identificacao_paciente=tipo_identificacao_paciente,
            numero_identificacao_paciente=numero_identificacao_paciente,
            hora=hora,
            data=data,
            protocolo=protocolo,
            status=status,
            registro_data_hora_atendimento=registro_data_hora_atendimento,
            usuario_responsavel_id=usuario_responsavel_id,
            usuario_responsavel_nome=usuario_responsavel_nome,
        )

class GetAgendamentos(BaseModel):

    
    agenda_id: UUID = Field(None, description="Chave estrangeira referenciando a Agenda")
    vacina: str | None = Field(None, description="Nome da vacina a ser aplicada")
    tipo_identificacao_paciente: str = Field(None, description="Tipo de identificação do paciente")
    numero_identificacao_paciente: str = Field(None, description="Número de identificação do paciente")
    hora: time = Field(None, description="Hora do agendamento")
    data: date = Field(None, description="Data do agendamento")
    protocolo: str | None = Field(None, description="Protocolo do agendamento")
    status: str | None = Field(None, description="Status do agendamento")
    registro_data_hora_atendimento: datetime | None = Field(None, description="Data e hora do atendimento registrado")
    usuario_responsavel_id: UUID | None = Field(None, description="Chave estrangeira referenciando o Usuário Responsável")
    usuario_responsavel_nome: str | None = Field(None, description="Nome do usuário responsável pelo atendimento")
    id: UUID = Field(None, description="Identificador único universal (UUIDv4) da entidade")
    criado_em: datetime = Field(None, description="Data e hora UTC da criação do registro")
    atualizado_em: datetime | None = Field(None, description="Data e hora UTC da última atualização do registro (null se nunca foi atualizado)")
    usuarios: GetUsuarios | None = Field(None)
    vacinas_aplicadas: list[GetVacinasAplicadas | None] = Field(None)
    
    model_config = ConfigDict(from_attributes=True)


class PatchAgendamentos(BaseModel):

    
    agenda_id: UUID | None = Field(None, description="Chave estrangeira referenciando a Agenda")
    vacina: str | None = Field(None, description="Nome da vacina a ser aplicada")
    tipo_identificacao_paciente: str | None = Field(None, description="Tipo de identificação do paciente")
    numero_identificacao_paciente: str | None = Field(None, description="Número de identificação do paciente")
    hora: time | None = Field(None, description="Hora do agendamento")
    data: date | None = Field(None, description="Data do agendamento")
    protocolo: str | None = Field(None, description="Protocolo do agendamento")
    status: str | None = Field(None, description="Status do agendamento")
    registro_data_hora_atendimento: datetime | None = Field(None, description="Data e hora do atendimento registrado")
    usuario_responsavel_id: UUID | None = Field(None, description="Chave estrangeira referenciando o Usuário Responsável")
    usuario_responsavel_nome: str | None = Field(None, description="Nome do usuário responsável pelo atendimento")

class AgendamentosInclude(str, Enum):
    agenda_id= "agenda_id"
    vacina= "vacina"
    tipo_identificacao_paciente= "tipo_identificacao_paciente"
    numero_identificacao_paciente= "numero_identificacao_paciente"
    hora= "hora"
    data= "data"
    protocolo= "protocolo"
    status= "status"
    registro_data_hora_atendimento= "registro_data_hora_atendimento"
    usuario_responsavel_id= "usuario_responsavel_id"
    usuario_responsavel_nome= "usuario_responsavel_nome"
    id= "id"
    criado_em= "criado_em"
    atualizado_em= "atualizado_em"

class AgendamentosExpand(str, Enum):
    usuarios = "usuarios"
    vacinas_aplicadas = "vacinas_aplicadas"
    agendas = "agendas"

class SortOp(str, Enum):
    asc = "ASC"
    desc = "DESC"


class CursorDirection(str, Enum):
    next = "next"
    prev = "prev"

def get_expand_query():
    """Retorna a configuração apropriada para o campo expand."""
    members = list(AgendamentosExpand.__members__.values())

    # Se não há membros (nunca acontecerá com o template atual)
    if not members:
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Se o único membro é "Nenhum"
    if len(members) == 1 and hasattr(AgendamentosExpand, "Nenhum"):
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Caso contrário, retorna os valores válidos (excluindo "Nenhum" se existir)
    valid_expansions = [
        m.value for m in members
        if not (hasattr(AgendamentosExpand, "Nenhum") and m == AgendamentosExpand.Nenhum)
    ]

    return Query(
        None,
        description="Relacionamentos a expandir",
        include_in_schema=True
    )


class QueryAgendamentos:
    def __init__(
        self,
        all_data: bool = Query(
            True,
            description="Retornar todas as correspondências ou apenas a primeira",
        ),
        # ==========================
        agenda_id: str | None = Query(None, description="Chave estrangeira referenciando a Agenda"),
        vacina: str | None = Query(None, description="Nome da vacina a ser aplicada"),
        tipo_identificacao_paciente: str | None = Query(None, description="Tipo de identificação do paciente"),
        numero_identificacao_paciente: str | None = Query(None, description="Número de identificação do paciente"),
        hora: str | None = Query(None, description="Hora do agendamento"),
        data: str | None = Query(None, description="Data do agendamento"),
        protocolo: str | None = Query(None, description="Protocolo do agendamento"),
        status: str | None = Query(None, description="Status do agendamento"),
        registro_data_hora_atendimento: str | None = Query(None, description="Data e hora do atendimento registrado"),
        usuario_responsavel_id: str | None = Query(None, description="Chave estrangeira referenciando o Usuário Responsável"),
        usuario_responsavel_nome: str | None = Query(None, description="Nome do usuário responsável pelo atendimento"),
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
        cursor_field: AgendamentosInclude = Query(
            AgendamentosInclude.id,
            description="Campo a ser usado como cursor (padrão: 'id')",
        ),
        cursor_direction: CursorDirection = Query(
            "next",
            description="Direção da paginação por cursor (next|prev)",
        ),
        # ==========================
        # Controle de retorno
        include: list[AgendamentosInclude] = Query(
            [], description="Atributos a incluir na resposta"
        ),
        exclude: list[AgendamentosInclude] = Query(
            [], description="Atributos a excluir da resposta"
        ),
        expand: list[AgendamentosExpand] | None = get_expand_query(),
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
        sort_field: AgendamentosInclude = Query(
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
        fields = [ f.value for f in AgendamentosInclude]
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


QueryAgendamentosDep = Annotated[QueryAgendamentos, Depends()]