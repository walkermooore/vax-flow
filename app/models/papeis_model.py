from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean, String

from app.db.base_class import Base


class Papeis(Base):
    """Modelo da tabela de Papéis (Roles) do sistema

    Representa um conjunto de permissões/funcionalidades que podem ser atribuídas a usuários.

    Atributos:
        nome (str): Nome identificador do papeis (ex: 'Admin', 'Gerente')
        ativo (bool): Indica se o papeis está ativo no sistema
        descricao (str): Descrição das permissões/funcionalidades do papeis
    """

    nome: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
        unique=True,
        comment="Nome identificador único do papeis (ex: 'Admin', 'Gerente')",
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        comment="Indica se o papeis está ativo e disponível para atribuição",
    )

    descricao: Mapped[str | None] = mapped_column(
        String(250),
        comment="Descrição detalhada das permissões e responsabilidades do papeis",
    )

    # Relacionamentos
    usuarios: Mapped[list["Usuarios"]] = relationship(
        "Usuarios",
        back_populates="papeis",
    )

    papeis_funcionalidades: Mapped[list["PapeisFuncionalidades"]] = relationship(
        "PapeisFuncionalidades",
        back_populates="papeis",
    )
