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


class Agendas(Base):
    
    unidade_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("unidades.id"),
        nullable=False,
        comment="Chave estrangeira referenciando a Unidade"
    )
    titulo: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Título da agenda"
    )
    capacidade_diaria: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Capacidade diária de agendamentos"
    )
    hora_inicio: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Hora de início do atendimento"
    )
    hora_fim: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Hora de fim do atendimento"
    )
    data_inicio: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
        comment="Data de início da agenda"
    )
    data_fim: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
        comment="Data de fim da agenda"
    )
    dias_semana: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Dias da semana em que a agenda está ativa"
    )
    
    # Relationships
    agendas_vacinas = relationship("AgendasVacinas", backref="agendas", lazy="noload")
    agendamentos = relationship("Agendamentos", backref="agendas", lazy="noload")
