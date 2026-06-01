import enum
import uuid
from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.types import LargeBinary, String

from app.db.base_class import Base
 
from sqlalchemy import Enum
from enum import Enum
class Status(str, Enum):
    FECHADO = "fechado"
    ABERTO = "aberto"
    VENCIDO = "vencido"
    ESGOTADO = "esgotado"

class UnidadeValidade(str, Enum):
    DIAS = "dias"
    HORAS = "horas"

class Lotes(Base):
    
    vacina_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("vacinas.id"),
        nullable=False,
        comment="Chave estrangeira referenciando a Vacina"
    )
    fabricante: Mapped[str] = mapped_column(
        String(255),
        comment="Fabricante do lote"
    )
    quantidade_total: Mapped[int] = mapped_column(
        Integer,
        comment="Quantidade total de vacinas no lote"
    )
    validade_aberto: Mapped[int] = mapped_column(
        Integer,
        comment="Validade após abertura (em dias)"
    )
    validade_fechado: Mapped[DateTime] = mapped_column(
        DateTime,
        comment="Validade do lote fechado"
    )
    lote_numero: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        comment="Número do lote"
    )
    lote_quantidade_atual: Mapped[int | None] = mapped_column(
        Integer,
        comment="Quantidade atual de vacinas no lote"
    )
    lote_validade_fechado: Mapped[Date] = mapped_column(
        Date,
        comment="Data de validade do lote fechado"
    )
    unidade_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("unidades.id"),
        nullable=False,
        comment="Chave estrangeira referenciando a Unidade"
    )
    local_refrigerador: Mapped[str | None] = mapped_column(
        String(100),
        nullable=False,
        comment="Localização no refrigerador"
    )
    temperatura_vacina: Mapped[str | None] = mapped_column(
        String(50),
        nullable=False,
        comment="Temperatura de armazenamento"
    )
    local_posicao: Mapped[str | None] = mapped_column(
        String(100),
        nullable=False,
        comment="Posição no local de armazenamento"
    )
    user_id: Mapped[str | None] = mapped_column(
        String(50),
        comment="Resposável por abertura"
    )
    doses_utilizadas: Mapped[int | None] = mapped_column(
        Integer,
        comment="Quantidade de doses utilizadas"
    )
    data_abertura: Mapped[DateTime] = mapped_column(
        DateTime,
        comment="Coluna de data de abertura das vacinas"
    )
    motivo_abertura: Mapped[str | None] = mapped_column(
        String(250),
        comment="Relatar o motivo da abertura das vacinas"
    )
    data_descarte: Mapped[DateTime] = mapped_column(
        DateTime,
        comment="Coluna de data de descarte das vacinas"
    )
    motivo_descarte: Mapped[str | None] = mapped_column(
        String(250),
        comment="Relatar o motivo da descarte das vacinas"
    )
    codigo_barras: Mapped[str | None] = mapped_column(
        String(255),
        comment="Código de barras do lote"
    )
    doses_por_frasco: Mapped[int | None] = mapped_column(
        Integer,
        comment="Quantidade de doses por frasco"
    )
    data_fabricacao: Mapped[DateTime | None] = mapped_column(
        DateTime,
        comment="Data de fabricação do lote"
    )
    status: Mapped[str] = mapped_column(
        String(255),
        comment="Fabricante do lote"
    ) 
    unidade_validade: Mapped[str] = mapped_column(
        String(255),
        comment="Fabricante do lote"
    )
    #unidade_validade: Mapped[UnidadeValidade | None] = mapped_column(
    #SQLEnum(UnidadeValidade, name="unidade_validade_enum"),
    #comment="Unidade de validade após abertura (dias ou horas)"
    # )
    #id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # status: Mapped[Status] = mapped_column(
        # SQLEnum(Status, name="status_Enum"),
      #  nullable=True
    #)
    vacinas_aplicadas = relationship("VacinasAplicadas", backref="lotes", lazy="noload")
