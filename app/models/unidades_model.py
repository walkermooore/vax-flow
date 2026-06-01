import enum
from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, Time, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.types import LargeBinary, String

from app.db.base_class import Base


class Unidades(Base):
   
    endereco_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("enderecos.id"),
        comment="Chave estrangeira referenciando o Endereço"
    )
    nome: Mapped[str] = mapped_column(
        String(255),
        comment="Nome da unidade"
    )
    nome_usuario_responsavel: Mapped[str | None] = mapped_column(
        String(255),
        comment="Nome do usuário responsável pela unidade"
    )
    tipo: Mapped[str | None] = mapped_column(
        String(100),
        comment="Tipo da unidade"
    )
    codigo_cnes: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        comment="Código CNES da unidade"
    )
    contato: Mapped[str | None] = mapped_column(
        String(50),
        comment="Contato da unidade"
    )
    email_unidade: Mapped[str | None] = mapped_column(
        String(255),
        comment="E-mail da unidade"
    )
    status: Mapped[str | None] = mapped_column(
        String(50),
        comment="Status da unidade"
    )
    capacidade_pacientes: Mapped[str | None] = mapped_column(
        String(100),
        comment="Capacidade de pacientes da unidade"
    )
    horario_funcionamento: Mapped[str | None] = mapped_column(
        String(100),
        comment="Horário de funcionamento da unidade"
    )
    informacoes_servico: Mapped[str | None] = mapped_column(
        Text,
        comment="Informações sobre os serviços da unidade"
    )
    
    # Relationships
    enderecos = relationship("Enderecos", backref="unidades", lazy="noload")
    agendas = relationship("Agendas", backref="unidades", lazy="noload")
    lotes = relationship("Lotes", backref="unidades", lazy="noload")
    usuarios = relationship("Usuarios", backref="unidades", lazy="noload")
    campanhas_unidades = relationship("CampanhasUnidades", backref="unidades", lazy="noload")
