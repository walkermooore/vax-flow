from datetime import datetime, date, time
from enum import Enum
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Form, Query
from pydantic import BaseModel, Field, ConfigDict, model_validator

from app.util import parse_operator_and_value
from app.core import ApiError

from .base_schema import *

from .vacinas_aplicadas_schema import GetVacinasAplicadas

from app.models.lotes_model import Status, UnidadeValidade




__all__ = [
    "PostLotes",
    "GetLotes",
    "PatchLotes",
    "QueryLotesDep",
]


class PostLotes(BaseModel):

    
    vacina_id: UUID  = Field(..., description="Chave estrangeira referenciando a Vacina")
    fabricante: str  = Field(..., description="Fabricante do lote")
    quantidade_total: int  = Field(..., description="Quantidade total de vacinas no lote")
    validade_aberto: int  = Field(..., description="Validade após abertura (em dias)")
    validade_fechado: datetime  = Field(..., description="Validade do lote fechado")
    lote_numero: str  = Field(..., description="Número do lote")
    lote_quantidade_atual: int | None  = Field(None, description="Quantidade atual de vacinas no lote")
    lote_validade_fechado: date  = Field(..., description="Data de validade do lote fechado")
    unidade_id: UUID  = Field(..., description="Chave estrangeira referenciando a Unidade")
    local_refrigerador: str  = Field(..., description="Localização no refrigerador")
    temperatura_vacina: str  = Field(..., description="Temperatura de armazenamento")
    local_posicao: str  = Field(..., description="Posição no local de armazenamento")
    
                        ## novos atributos adicionados##
    user_id: str | None = Field(..., description="Responsável pela abertura do lote")
    doses_utilizadas: int | None = Field(..., description="Quantidade de doses utilizadas")
    data_abertura: datetime | None = Field(..., description="Data de abertura do lote")
    motivo_abertura: str | None = Field(..., description="Motivo da abertura do lote")
    data_descarte: datetime | None = Field(..., description="Data de descarte do lote")
    motivo_descarte: str | None = Field(..., description="Motivo do descarte do lote")
    codigo_barras: str | None = Field(..., description="Código de barras do lote")
    doses_por_frasco: int | None = Field(..., description="Quantidade de doses por frasco")
    data_fabricacao: datetime | None = Field(..., description="Data de fabricação do lote")
    unidade_validade: UnidadeValidade | None = Field(..., description="Unidade de validade após abertura (dias ou horas)")
    status: Status = Field(..., description="Status do lote")



    @model_validator(mode="before")
    @classmethod
    def validators_lotes(self, data) -> "PostLotes":
        if not "lote_numero" in data:
            raise ValueError("É necessário informar o lote_numero para prosseguir.")
        return data

    @classmethod
    def as_form(
        cls,
        vacina_id: UUID = Form(..., description="Chave estrangeira referenciando a Vacina"),
        fabricante: str = Form(..., description="Fabricante do lote"),
        quantidade_total: int = Form(..., description="Quantidade total de vacinas no lote"),
        validade_aberto: int = Form(..., description="Validade após abertura (em dias)"),
        validade_fechado: datetime = Form(..., description="Validade do lote fechado"),
        lote_numero: str = Form(..., description="Número do lote"),
        lote_quantidade_atual: int | None = Form(None, description="Quantidade atual de vacinas no lote"),
        lote_validade_fechado: date = Form(..., description="Data de validade do lote fechado"),
        unidade_id: UUID = Form(..., description="Chave estrangeira referenciando a Unidade"),
        local_refrigerador: str = Form(..., description="Localização no refrigerador"),
        temperatura_vacina: str = Form(..., description="Temperatura de armazenamento"),
        local_posicao: str = Form(..., description="Posição no local de armazenamento"),
                       ## novos atributos adicionados##
         
        user_id: int = Form(..., description="Responsável pela abertura do lote"),
        doses_utilizadas: int = Form(..., description="Quantidade de doses utilizadas"),
        data_abertura: datetime = Form(..., description="Data de abertura do lote"),
        motivo_abertura: str = Form(..., description="Motivo da abertura do lote"),
        data_descarte: datetime = Form(..., description="Data de descarte do lote"),
        motivo_descarte: str = Form(..., description="Motivo do descarte do lote"),
        codigo_barras: str = Form(..., description="Código de barras do lote"),
        doses_por_frasco: int = Form(..., description="Quantidade de doses por frasco"),
        data_fabricacao: datetime = Form(..., description="Data de fabricação do lote"),
        unidade_validade: UnidadeValidade = Form(..., description="Status do lote"),
        status: Status = Form(..., description="Status do lote"),
    ):
        return cls(
            vacina_id=vacina_id,
            fabricante=fabricante,
            quantidade_total=quantidade_total,
            validade_aberto=validade_aberto,
            validade_fechado=validade_fechado,
            lote_numero=lote_numero,
            lote_quantidade_atual=lote_quantidade_atual,
            lote_validade_fechado=lote_validade_fechado,
            unidade_id=unidade_id,
            local_refrigerador=local_refrigerador,
            temperatura_vacina=temperatura_vacina,
            local_posicao=local_posicao,
            
            ## novos atributos adicionados##
            user_id=user_id,
            doses_utilizadas=doses_utilizadas,
            data_abertura=data_abertura,
            motivo_abertura=motivo_abertura,
            data_descarte=data_descarte,
            motivo_descarte=motivo_descarte,
            codigo_barras=codigo_barras,
            doses_por_frasco=doses_por_frasco,
            data_fabricacao=data_fabricacao,
            unidade_validade=unidade_validade,
            status=status,
        )

class GetLotes(BaseModel):

    vacina_id: UUID = Field(None, description="Chave estrangeira referenciando a Vacina")
    fabricante: str = Field(None, description="Fabricante do lote")
    quantidade_total: int = Field(None, description="Quantidade total de vacinas no lote")
    validade_aberto: int = Field(None, description="Validade após abertura (em dias)")
    validade_fechado: datetime = Field(None, description="Validade do lote fechado")
    lote_numero: str = Field(None, description="Número do lote")
    lote_quantidade_atual: int | None = Field(None, description="Quantidade atual de vacinas no lote")
    lote_validade_fechado: date = Field(None, description="Data de validade do lote fechado")
    unidade_id: UUID = Field(None, description="Chave estrangeira referenciando a Unidade")
    local_refrigerador: str = Field(None, description="Localização no refrigerador")
    temperatura_vacina: str = Field(None, description="Temperatura de armazenamento")
    local_posicao: str = Field(None, description="Posição no local de armazenamento")
    id: UUID = Field(None, description="Identificador único universal (UUIDv4) da entidade")
    criado_em: datetime = Field(None, description="Data e hora UTC da criação do registro")
    atualizado_em: datetime | None = Field(None, description="Data e hora UTC da última atualização do registro (null se nunca foi atualizado)")
    vacinas_aplicadas: list[GetVacinasAplicadas | None] = Field(None)
    
    model_config = ConfigDict(from_attributes=True)
    
                   ## novos atributos adicionados##
    user_id: str | None = Field(None, description="Responsável pela abertura do lote")
    doses_utilizadas: int | None = Field(None, description="Quantidade de doses utilizadas")
    data_abertura: datetime | None = Field(None, description="Data de abertura do lote")
    motivo_abertura: str | None = Field(None, description="Motivo da abertura do lote")
    data_descarte: datetime | None = Field(None, description="Data de descarte do lote")
    motivo_descarte: str | None = Field(None, description="Motivo do descarte do lote")
    codigo_barras: str | None = Field(None, description="Código de barras do lote")
    doses_por_frasco: int | None = Field(None, description="Quantidade de doses por frasco")
    data_fabricacao: datetime | None = Field(None, description="Data de fabricação do lote")
    unidade_validade: UnidadeValidade | None = Field(None, description="Unidade de validade após abertura (dias ou horas)")
    status: Status | None = Field(None, description="Status do lote")




class PatchLotes(BaseModel):

    
    vacina_id: UUID | None = Field(None, description="Chave estrangeira referenciando a Vacina")
    fabricante: str | None = Field(None, description="Fabricante do lote")
    quantidade_total: int | None = Field(None, description="Quantidade total de vacinas no lote")
    validade_aberto: int | None = Field(None, description="Validade após abertura (em dias)")
    validade_fechado: datetime | None = Field(None, description="Validade do lote fechado")
    lote_numero: str | None = Field(None, description="Número do lote")
    lote_quantidade_atual: int | None = Field(None, description="Quantidade atual de vacinas no lote")
    lote_validade_fechado: date | None = Field(None, description="Data de validade do lote fechado")
    unidade_id: UUID | None = Field(None, description="Chave estrangeira referenciando a Unidade")
    local_refrigerador: str | None = Field(None, description="Localização no refrigerador")
    temperatura_vacina: str | None = Field(None, description="Temperatura de armazenamento")
    local_posicao: str | None = Field(None, description="Posição no local de armazenamento")
    
             ## novos atributos adicionados##
    user_id: str | None = Field(None, description="Responsável pela abertura do lote")
    doses_utilizadas: int | None = Field(None, description="Quantidade de doses utilizadas")
    data_abertura: datetime | None = Field(None, description="Data de abertura do lote")
    motivo_abertura: str | None = Field(None, description="Motivo da abertura do lote")
    data_descarte: datetime | None = Field(None, description="Data de descarte do lote")
    motivo_descarte: str | None = Field(None, description="Motivo do descarte do lote")
    codigo_barras: str | None = Field(None, description="Código de barras do lote")
    doses_por_frasco: int | None = Field(None, description="Quantidade de doses por frasco")
    data_fabricacao: datetime | None = Field(None, description="Data de fabricação do lote")
    unidade_validade: UnidadeValidade | None = Field(None, description="Unidade de validade após abertura (dias ou horas)")
    status:Status | None = Field(None, description="Status do lote")



class LotesInclude(str, Enum):
    vacina_id= "vacina_id"
    fabricante= "fabricante"
    quantidade_total= "quantidade_total"
    validade_aberto= "validade_aberto"
    validade_fechado= "validade_fechado"
    lote_numero= "lote_numero"
    lote_quantidade_atual= "lote_quantidade_atual"
    lote_validade_fechado= "lote_validade_fechado"
    unidade_id= "unidade_id"
    local_refrigerador= "local_refrigerador"
    temperatura_vacina= "temperatura_vacina"
    local_posicao= "local_posicao"
    id= "id"
    criado_em= "criado_em"
    atualizado_em= "atualizado_em"

     ## novos atributos adicionados##
    user_id = "user_id"
    doses_utilizadas = "doses_utilizadas"
    data_abertura = "data_abertura"
    motivo_abertura = "motivo_abertura"
    data_descarte = "data_descarte"
    motivo_descarte = "motivo_descarte"
    codigo_barras = "codigo_barras"
    doses_por_frasco = "doses_por_frasco"
    data_fabricacao = "data_fabricacao"
    unidade_validade = "unidade_validade"
    status = "status"

class LotesExpand(str, Enum):
    vacinas_aplicadas = "vacinas_aplicadas"
    unidades = "unidades"
    vacinas = "vacinas"

class SortOp(str, Enum):
    asc = "ASC"
    desc = "DESC"


class CursorDirection(str, Enum):
    next = "next"
    prev = "prev"

def get_expand_query():
    """Retorna a configuração apropriada para o campo expand."""
    members = list(LotesExpand.__members__.values())

    # Se não há membros (nunca acontecerá com o template atual)
    if not members:
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Se o único membro é "Nenhum"
    if len(members) == 1 and hasattr(LotesExpand, "Nenhum"):
        return Query(
            None,
            include_in_schema=False,
            description="Este endpoint não possui relacionamentos expansíveis"
        )

    # Caso contrário, retorna os valores válidos (excluindo "Nenhum" se existir)
    valid_expansions = [
        m.value for m in members
        if not (hasattr(LotesExpand, "Nenhum") and m == LotesExpand.Nenhum)
    ]

    return Query(
        None,
        description="Relacionamentos a expandir",
        include_in_schema=True
    )


class QueryLotes:
    def __init__(
        self,
        all_data: bool = Query(
            True,
            description="Retornar todas as correspondências ou apenas a primeira",
        ),
        # ==========================
        vacina_id: UUID | None = Query(None, description="Chave estrangeira referenciando a Vacina"),
        fabricante: str | None = Query(None, description="Fabricante do lote"),
        quantidade_total: int | None = Query(None, description="Quantidade total de vacinas no lote"),
        validade_aberto: datetime | None = Query(None, description="Validade após abertura (em dias)"),
        validade_fechado: datetime | None = Query(None, description="Validade do lote fechado"),
        lote_numero: str | None = Query(None, description="Número do lote"),
        lote_quantidade_atual: int | None = Query(None, description="Quantidade atual de vacinas no lote"),
        lote_validade_fechado: datetime | None = Query(None, description="Data de validade do lote fechado"),
        unidade_id: int | None = Query(None, description="Chave estrangeira referenciando a Unidade"),
        local_refrigerador: str | None = Query(None, description="Localização no refrigerador"),
        temperatura_vacina: str | None = Query(None, description="Temperatura de armazenamento"),
        local_posicao: str | None = Query(None, description="Posição no local de armazenamento"),
        id: int | None = Query(None, description="Identificador único universal (UUIDv4) da entidade"),
        criado_em: str | None = Query(None, description="Data e hora UTC da criação do registro"),
        atualizado_em: str | None = Query(None, description="Data e hora UTC da última atualização do registro (null se nunca foi atualizado)"),
        
        ## novos atributos adicionados##
        user_id: int | None = Query(None, description="Responsável pela abertura do lote"),
        doses_utilizadas: int | None = Query(None, description="Quantidade de doses utilizadas"),
        data_abertura: datetime | None = Query(None, description="Data de abertura do lote"),
        motivo_abertura: str | None = Query(None, description="Motivo da abertura do lote"),
        data_descarte: datetime | None = Query(None, description="Data de descarte do lote"),
        motivo_descarte: str | None = Query(None, description="Motivo do descarte do lote"),
        codigo_barras: str | None = Query(None, description="Código de barras do lote"),
        doses_por_frasco: int | None = Query(None, description="Quantidade de doses por frasco"),
        data_fabricacao: datetime | None = Query(None, description="Data de fabricação do lote"),
        unidade_validade: UnidadeValidade | None = Query(None, description="Unidade de validade após abertura (dias ou horas)"),
        status: Status | None = Query(None, description="Status do lote"),
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
        cursor_field: LotesInclude = Query(
            LotesInclude.id,
            description="Campo a ser usado como cursor (padrão: 'id')",
        ),
        cursor_direction: CursorDirection = Query(
            "next",
            description="Direção da paginação por cursor (next|prev)",
        ),
        # ==========================
        # Controle de retorno
        include: list[LotesInclude] = Query(
            [], description="Atributos a incluir na resposta"
        ),
        exclude: list[LotesInclude] = Query(
            [], description="Atributos a excluir da resposta"
        ),
        expand: list[LotesExpand] | None = get_expand_query(),
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
        sort_field: LotesInclude = Query(
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
        fields = [ f.value for f in LotesInclude]
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


QueryLotesDep = Annotated[QueryLotes, Depends()]