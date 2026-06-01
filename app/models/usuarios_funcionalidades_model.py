from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class UsuariosFuncionalidades(Base):

    usuario_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id"),
        primary_key=True,
        comment="Chave estrangeira referenciando o ID do Usuário",
    )
    funcionalidade_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("funcionalidades.id"),
        primary_key=True,
        comment="Chave estrangeira referenciando o ID da Funcionalidades",
    )
    funcionalidades: Mapped["Funcionalidades"] = relationship(
        "Funcionalidades",
        back_populates="usuarios_funcionalidades",
        lazy="noload",
    )
    usuarios: Mapped["Usuarios"] = relationship(
        "Usuarios",
        back_populates="usuarios_funcionalidades",
    )
