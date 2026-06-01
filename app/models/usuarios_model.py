from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean, LargeBinary, String

from app.db.base_class import Base


class Usuarios(Base):
    
    nome_usuario: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        comment="Nome de usuário para login"
    )
    nome_completo: Mapped[str] = mapped_column(
        String(255),
        comment="Nome completo do usuário"
    )
    telefone: Mapped[str | None] = mapped_column(
        String(20),
        comment="Telefone do usuário"
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        comment="E-mail do usuário"
    )
    senha: Mapped[bytes] = mapped_column(
        "senha",
        comment="Senha criptografada do usuário"
    )
    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        comment="Indica se o usuário está ativo"
    )
    papel_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("papeis.id"),
        comment="Chave estrangeira referenciando o Papel"
    )
    unidade_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("unidades.id"),
        comment="Chave estrangeira referenciando a Unidade"
    )
    cargo: Mapped[str | None] = mapped_column(
        String(100),
        comment="Cargo do usuário"
    )
    
    # Relationships
    papeis: Mapped["Papeis"] = relationship(
        "Papeis",
        back_populates="usuarios",
        lazy="noload",
    )
    usuarios_funcionalidades: Mapped[list["UsuariosFuncionalidades"]] = relationship(
        "UsuariosFuncionalidades",
        back_populates="usuarios",
        lazy="noload",
    )
   