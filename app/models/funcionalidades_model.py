from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean, DateTime, Integer, String

from app.db.base_class import Base


class Funcionalidades(Base):
    """Modelo da tabela de Funcionalidades da API

    Representa endpoints/operações disponíveis no sistema com seus metadados.
    """

    chave: Mapped[int | None] = mapped_column(
        Integer(),
        primary_key=True,
        autoincrement=True,
        comment="Chave de acesso autoincrementada",
    )
    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Nome amigável da funcionalidades (ex: 'Excluir Cliente')",
    )
    escopo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        comment="Identificador único no formato 'recurso:ação' (ex: 'client:delete')",
    )
    caminho: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Endpoint da API (ex: '/api/client/{id}')",
    )
    metodo: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Método HTTP (GET, POST, PUT, DELETE, etc)",
    )
    descricao: Mapped[str | None] = mapped_column(
        String(500),
        comment="Descrição detalhada do propósito da funcionalidades",
    )
    categoria: Mapped[str | None] = mapped_column(
        String(50),
        comment="Grupo funcional (ex: 'CRM', 'Financeiro', 'Relatórios')",
    )
    sensivel: Mapped[bool | None] = mapped_column(
        Boolean(),
        default=False,
        comment="Indica se é uma operação crítica/cuidado extra necessário",
    )
    versao: Mapped[int | None] = mapped_column(
        Integer(),
        default=1,
        comment="Versão da funcionalidades para controle de evolução",
    )

    # Relacionamentos (mantive os nomes anteriores por não saber seu contexto)
    papeis_funcionalidades: Mapped[list["PapeisFuncionalidades"]] = relationship(
        "PapeisFuncionalidades", back_populates="funcionalidades"
    )
    usuarios_funcionalidades: Mapped[list["UsuariosFuncionalidades"]] = relationship(
        "UsuariosFuncionalidades", back_populates="funcionalidades"
    )
