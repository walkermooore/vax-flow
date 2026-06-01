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


class Vacinas(Base):
    
    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        comment="Nome da vacina"
    )
    # Relationships
    lotes = relationship("Lotes", backref="vacinas", lazy="noload")
    agendas_vacinas = relationship("AgendasVacinas", backref="vacinas", lazy="noload")
