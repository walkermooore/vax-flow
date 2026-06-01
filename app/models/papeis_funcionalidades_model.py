from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class PapeisFuncionalidades(Base):
    """Tabela de associação entre Papéis e Funcionalidades

    Representa as permissões específicas que um papeis tem sobre uma funcionalidades do sistema.

    Atributos:
        papel_id (UUID): Chave estrangeira para o Papeis
        funcionalidade_id (UUID): Chave estrangeira para a Funcionalidades
    """

    papel_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("papeis.id"),
        primary_key=True,
        comment="Chave estrangeira referenciando o ID do Papeis",
    )

    funcionalidade_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("funcionalidades.id"),
        primary_key=True,
    )

    funcionalidades: Mapped["Funcionalidades"] = relationship(
        "Funcionalidades",
        back_populates="papeis_funcionalidades",
        lazy="noload",
    )

    papeis: Mapped["Papeis"] = relationship(
        "Papeis",
        back_populates="papeis_funcionalidades",
        lazy="noload",
    )
