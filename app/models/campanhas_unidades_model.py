import enum
import uuid
from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean

from app.db.base_class import Base


class CampanhasUnidades(Base):
    
    campanha_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("campanhas.id"),
        primary_key=True,
        comment="Chave estrangeira referenciando a Campanha"
    )
    unidade_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("unidades.id"),
        primary_key=True,
        comment="Chave estrangeira referenciando a Unidade"
    )
