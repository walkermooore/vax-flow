import enum
import uuid
from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.types import LargeBinary, String, Text

from app.db.base_class import Base


class Campanhas(Base):
    
    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome da campanha"
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Status da campanha"
    )
    doses_aplicadas: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="Quantidade de doses aplicadas na campanha"
    )
    data_inicio: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
        comment="Data de início da campanha"
    )
    data_fim: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
        comment="Data de fim da campanha"
    )
    publico_alvo: Mapped[str | None] = mapped_column(
        String(255),
        nullable=False,
        comment="Público-alvo da campanha"
    )
    meta_vacinacao: Mapped[int | None] = mapped_column(
        Integer,
        nullable=False,
        comment="Meta de vacinação da campanha"
    )
    descricao: Mapped[str] = mapped_column(
        Text,
        comment="Descrição da campanha"
    )
    horario_funcionamento: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Horário de funcionamento da campanha"
    )
    endereco_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("enderecos.id"),
        nullable=False,
        comment="Chave estrangeira referenciando o Endereço"
    )
    
    # Relationships
    enderecos = relationship("Enderecos", backref="campanhas", lazy="noload")
    campanhas_unidades = relationship("CampanhasUnidades", backref="campanhas", lazy="noload")
