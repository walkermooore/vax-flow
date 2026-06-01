from sqlalchemy import (Boolean, Date, DateTime, Float, ForeignKey, Integer,
                        String, Text, Time)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class VacinasAplicadas(Base):
    
    lote_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lotes.id"),
        nullable=False,
        comment="Chave estrangeira referenciando o Lote"
    )
    agendamento_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agendamentos.id"),
        nullable=False,
        comment="Chave estrangeira referenciando o Agendamento"
    )
