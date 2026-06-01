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


class AgendasVacinas(Base):
    
    vacina_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("vacinas.id"),
        primary_key=True,
        comment="Chave estrangeira referenciando a Vacina"
    )
    agenda_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agendas.id"),
        primary_key=True,
        comment="Chave estrangeira referenciando a Agenda"
    )
