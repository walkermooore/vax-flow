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


class Enderecos(Base):
    
    nomeLocal: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do local"
    )
    logradouro: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Logradouro do endereço"
    )
    numero: Mapped[str | None] = mapped_column(
        String(20),
        nullable=False,
        comment="Número do endereço"
    )
    complemento: Mapped[str | None] = mapped_column(
        String(100),
        comment="Complemento do endereço"
    )
    bairro: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Bairro do endereço"
    )
    cep: Mapped[str | None] = mapped_column(
        String(10),
        nullable=False,
        comment="CEP do endereço"
    )
    cidade: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Cidade do endereço"
    )
    estado: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
        comment="Estado do endereço"
    )
    latitude: Mapped[float] = mapped_column(
        Float,
        comment="Latitude geográfica"
    )
    longitude: Mapped[float] = mapped_column(
        Float,
        comment="Longitude geográfica"
    )
