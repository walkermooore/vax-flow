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


class Agendamentos(Base):
       
    agenda_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agendas.id"),
        comment="Chave estrangeira referenciando a Agenda"
    )
    vacina: Mapped[str | None] = mapped_column(
        String(255),
        comment="Nome da vacina a ser aplicada"
    )
    tipo_identificacao_paciente: Mapped[str] = mapped_column(
        String(50),
        comment="Tipo de identificação do paciente"
    )
    numero_identificacao_paciente: Mapped[str] = mapped_column(
        String(100),
        comment="Número de identificação do paciente"
    )
    hora: Mapped[Time] = mapped_column(
        Time,
        comment="Hora do agendamento"
    )
    data: Mapped[Date] = mapped_column(
        Date,
        comment="Data do agendamento"
    )
    protocolo: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        comment="Protocolo do agendamento"
    )
    status: Mapped[str | None] = mapped_column(
        String(50),
        comment="Status do agendamento"
    )
    registro_data_hora_atendimento: Mapped[DateTime | None] = mapped_column(
        DateTime,
        comment="Data e hora do atendimento registrado"
    )
    usuario_responsavel_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id"),
        comment="Chave estrangeira referenciando o Usuário Responsável"
    )
    usuario_responsavel_nome: Mapped[str | None] = mapped_column(
        String(255),
        comment="Nome do usuário responsável pelo atendimento"
    )
    
    # Relationships
    usuarios = relationship("Usuarios", backref="agendamentos", lazy="noload")
    vacinas_aplicadas = relationship("VacinasAplicadas", backref="agendamentos", lazy="noload")


