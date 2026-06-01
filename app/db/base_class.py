import re
import uuid
from datetime import datetime
from enum import Enum
from math import ceil
from typing import Any, Dict, Union
from uuid import UUID

from sqlalchemy import VARCHAR, DateTime, String, func, select
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.exc import (DataError, IntegrityError, OperationalError,
                            SQLAlchemyError)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import (DeclarativeBase, Mapped, RelationshipProperty,
                            Session, joinedload, mapped_column, selectinload)

from app import core, util
from app.core import ApiError, ApiSuccess, Meta

__all__ = ["Base"]


def generate_id():
    return str(uuid.uuid4())


type_mapping = {
    "lk": [str],
    "in": [
        int,
        float,
        lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        lambda x: datetime.strptime(x, "%H:%M:%S").time(),
    ],
    "lt": [
        int,
        float,
        lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        lambda x: datetime.strptime(x, "%H:%M:%S").time(),
    ],
    "gt": [
        int,
        float,
        lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        lambda x: datetime.strptime(x, "%H:%M:%S").time(),
    ],
    "le": [
        int,
        float,
        lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        lambda x: datetime.strptime(x, "%H:%M:%S").time(),
    ],
    "ge": [
        int,
        float,
        lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        lambda x: datetime.strptime(x, "%H:%M:%S").time(),
    ],
}


def convert_value(value, types):
    """Tenta converter um valor em uma lista de tipos especificados."""
    for conversion_fn in types:
        try:
            return conversion_fn(value)
        except Exception as e:
            raise ApiError(
                status_code=404,
                loc=["body", value],
                msg=f"O valor deve estar em um formato compatível com inteiros, floats, datas ou tempos.",
                type="value_error.core.security",
            )


class Base(DeclarativeBase):
    """Classe base para todos os modelos do SQLAlchemy.
    Fornece campos padrão que serão herdados por todas as entidades do sistema:
    - ID único (UUID)
    - Timestamps de criação e atualização
    """

    __name__: str  # Nome da tabela no banco de dados

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        unique=True,
        primary_key=True,
        default=generate_id,
        comment="Identificador único universal (UUIDv4) da entidade",
    )

    criado_em: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="Data e hora UTC da criação do registro",
    )

    atualizado_em: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=True,
        onupdate=datetime.now,
        comment="Data e hora UTC da última atualização do registro (null se nunca foi atualizado)",
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return util.pascal_to_snake_case(cls.__name__)

    @declared_attr
    def __table_args__(cls):
        return {"schema": None}

    @staticmethod
    def _extract_column_from_constraint(constraint_name: str) -> str:
        """Extrai o nome da coluna a partir do nome da constraint de unicidade."""
        if not constraint_name:
            return None

        # Primeiro limpa a string removendo detalhes extras e quebras de linha
        clean_constraint = constraint_name.split("\n")[0].strip('"').strip()

        # Padrões regex melhorados
        patterns = [
            r"(?:^|_)([a-z]+)_(?:key|uniq|ix|uq|uk)$",  # user_username_key → nome_usuario
            r"(?:^|_)([a-z]+)$",  # nome_usuario → nome_usuario
        ]

        for pattern in patterns:
            match = re.search(pattern, clean_constraint.lower())
            if match:
                return match.group(1)

        return clean_constraint

    def create(
        self, session: Session, response_data: bool = True
    ) -> ApiSuccess | ApiError:
        """Cria um novo registro no banco de dados."""
        try:
            data = self
            session.add(data)
            session.flush()
            session.commit()
            session.refresh(data)
            if not response_data:
                return ApiSuccess(msg="OK")
            return data

        except IntegrityError as ie:
            session.rollback()
            error_msg = str(ie.orig).lower()

            # Tratamento para erro de chave estrangeira
            if (
                "foreign key" in error_msg
                or "violates foreign key constraint" in error_msg
            ):
                column_name = None
                patterns = [
                    r'violates foreign key constraint "[^"]+" on table "[^"]+"\nDETAIL:  Key \(([^)]+)\)=\([^)]+\) is not present in table',
                    r'violates foreign key constraint "[^"]+"\nDETAIL:  Key \(([^)]+)\)=\([^)]+\) is not present in table',
                    r'foreign key violation: "([^"]+)"',
                    r'column "([^"]+)" references',
                ]

                for pattern in patterns:
                    match = re.search(pattern, str(ie.orig), re.IGNORECASE)
                    if match:
                        column_name = match.group(1)
                        break

                if column_name:
                    column_name = column_name.strip('"')
                    friendly_name = column_name.replace("_id", "").replace("_", " ")
                    raise ApiError(
                        status_code=422,
                        loc=["body", column_name],
                        msg=f"{friendly_name} não foi encontrado",
                        type="db.foreign_key",
                    )
                else:
                    raise ApiError(
                        status_code=422,
                        loc=["body"],
                        msg="Referência inválida - um dos UUIDs não foi encontrado",
                        type="db.foreign_key",
                    )

            # Tratamento para erro de unicidade
            elif "unique" in error_msg or "duplicate key" in error_msg:
                constraint_name = None
                column_name = None

                if "violates unique constraint" in error_msg:
                    parts = error_msg.split("violates unique constraint")[1].split(" ")
                    if len(parts) > 1:
                        constraint_name = parts[1].strip('"')
                        column_name = self._extract_column_from_constraint(
                            constraint_name
                        )

                if column_name:
                    raise ApiError(
                        status_code=422,
                        loc=["body", column_name],
                        msg=f"Já existe um registro com este valor para {column_name.replace('_', ' ')}",
                        type="db.unique",
                    )
                else:
                    raise ApiError(
                        status_code=422,
                        loc=["body"],
                        msg="Violação de constraint única",
                        type="db.unique",
                    )

            # Outros erros de integridade
            raise ApiError(
                status_code=422,
                loc=["body"],
                msg=f"Erro de integridade no banco de dados: {str(ie.orig)}",
                type="db.integrity",
            )

        except DataError as de:
            session.rollback()
            error_msg = str(de.orig)

            # Tratamento para StringDataRightTruncation (valor muito longo)
            if (
                "value too long for type" in error_msg.lower()
                or "string data right truncation" in error_msg.lower()
            ):
                # Padrões para extrair o nome da coluna
                patterns = [
                    r'column "(.*?)".*?type character varying\((\d+)\)',  # PostgreSQL
                    r'value too long for type (?:varchar|character varying)\((\d+)\) of column "(.*?)"',  # Outros dialetos
                    r'column "(.*?)".*?exceeds maximum length of (\d+)',  # Padrão alternativo
                ]

                column_name = None
                max_length = None

                for pattern in patterns:
                    match = re.search(pattern, error_msg, re.IGNORECASE)
                    if match:
                        # Alguns padrões capturam em ordem diferente
                        if "varying" in pattern:  # Primeiro padrão
                            column_name = match.group(1)
                            max_length = int(match.group(2))
                        else:  # Segundo padrão
                            max_length = int(match.group(1))
                            column_name = match.group(2)
                        break

                if column_name:
                    column_name = column_name.strip('"')
                    friendly_name = column_name.replace("_", " ")

                    raise ApiError(
                        status_code=422,
                        loc=["body", column_name],
                        msg=f"O campo '{friendly_name}' excede o tamanho máximo de {max_length} caracteres",
                        type="db.string_too_long",
                    )

                # Fallback para quando não conseguir extrair o nome da coluna
                # Vamos tentar encontrar o nome da coluna nos dados do modelo
                if hasattr(self, "__table__"):
                    for column in self.__table__.columns:
                        if isinstance(column.type, (String, VARCHAR)):
                            if (
                                column.type.length
                                and len(getattr(self, column.name, ""))
                                > column.type.length
                            ):
                                column_name = column.name
                                max_length = column.type.length
                                break

                if column_name:
                    friendly_name = column_name.replace("_", " ")
                    raise ApiError(
                        status_code=422,
                        loc=["body", column_name],
                        msg=f"O campo '{friendly_name}' excede o tamanho máximo de {max_length} caracteres",
                        type="db.string_too_long",
                    )
                else:
                    # Último fallback genérico (não deve acontecer se o modelo estiver correto)
                    raise ApiError(
                        status_code=422,
                        loc=["body"],
                        msg="Um ou mais campos excedem o tamanho máximo permitido",
                        type="db.string_too_long",
                    )

        # Outros erros de dados
        except SQLAlchemyError as e:
            raise ApiError(
                status_code=500,
                loc=["body"],
                msg=f"Erro no banco de dados: {str(e)}",
                type="db.database_error",
            )

        except Exception as e:
            raise ApiError(
                status_code=500,
                loc=["body"],
                msg=str(e),
                type="server_error",
            )

    @classmethod
    def login(cls, session: Session, attribute: str, value: Any, senha: str) -> object:
        """executa login em usuarios

        Args:
            attribute (str): Nome do atributo para verificar o valor
            value (str): nome_usuario para efetuar o login
            senha (str): senha para ser verificada

        Raises:
            CustomException: 404 usuarios ou senha incorretos
            CustomException: 401 status do usuarios inativo
            CustomException: 401 senha incorreta_

        Returns:
            object: _description_
        """

        if not hasattr(cls, attribute):
            raise ApiError(
                status_code=404,
                loc=["body", attribute],
                msg=f"Atributo '{attribute}' não encontrado na tabela",
                type="db.attribute_not_found",
            )

        data = session.query(cls).filter(getattr(cls, attribute) == value).first()
        if not data:
            raise ApiError(
                status_code=404,
                loc=["body", attribute],
                msg="Usuario ou senha inválidos",
                type="db.invalid_credentials",
            )
        if hasattr(data, "active"):
            if not data.active:
                raise ApiError(
                    status_code=401,
                    loc=["body"],
                    msg="Usuário inativo",
                    type="db.inactive_user",
                )
        # Verifica a senha
        if not hasattr(data, "senha"):
            raise ApiError(
                status_code=500,
                loc=["body"],
                msg="Configuração inválida do modelo de usuário",
                type="db.missing_password_field",
            )
        if not core.verify_password(senha, data.senha):
            raise ApiError(
                status_code=401,
                loc=["body", "senha"],
                msg="Credenciais inválidas",  # Mesma mensagem por segurança
                type="db.invalid_credentials",
            )
        return data

    @classmethod
    def query_params(
        cls,
        session: Session,
        # Controle de retorno de dados
        all_data: bool = False,
        count_only: bool = False,
        distinct: bool = False,
        # Filtros
        filters: Dict[str, Any] | None = None,
        # Paginação numérica
        limit: int | None = 10,
        offset: int | None = 0,
        # Paginação por cursor
        cursor: str | None = None,
        cursor_field: str = "id",
        cursor_direction: str = "next",  # 'next' ou 'prev'
        # Seleção de campos
        include: list[str] | None = None,
        exclude: list[str] | None = None,
        expand: list[str] | None = None,
        # Ordenação
        sort_op: str | None = None,
        sort_field: str | None = None,
    ) -> ApiSuccess[Dict[str, Any]]:
        """
        Realiza consultas personalizadas com suporte a:
        - Filtros avançados
        - Paginação por offset ou cursor
        - Seleção de campos (include/exclude)
        - Expansão de relacionamentos
        - Ordenação dinâmica
        - Metadados de paginação

        Regras:
        - Não é permitido usar `include` com `expand` (joinedload exige o modelo completo).
        - `include` e `exclude` são mutuamente exclusivos.

        Args:
            session: Sessão SQLAlchemy
            all_data: Ignora paginação e retorna todos os dados
            count_only: Retorna apenas contagem
            distinct: Aplica DISTINCT na query
            filters: Filtros {campo: valor ou operador}
            limit: Limite por página
            offset: Deslocamento manual
            cursor: Valor de cursor para paginação sequencial
            cursor_field: Campo base para o cursor
            cursor_direction: 'next' ou 'prev'
            include: Lista de campos a incluir (colunas explícitas)
            exclude: Lista de campos a excluir (restantes do modelo)
            expand: Relacionamentos a expandir com joinedload
            sort_op: ASC ou DESC
            sort_field: Campo base da ordenação

        Returns:
            ApiSuccess com dados e metadados de paginação
        """
        try:
            limit = 10 if limit is None else limit
            offset = 0 if offset is None else offset
            # Validadores iniciais

            if include and expand:
                raise ApiError(
                    status_code=400,
                    loc=["query"],
                    msg="Não é possível usar 'include' junto com 'expand'. Use a seleção completa da entidade para expandir relacionamentos.",
                    type="db.invalid_include_expand_combination",
                )
            if exclude and expand:
                raise ApiError(
                    status_code=400,
                    loc=["query"],
                    msg="Não é possível usar 'exclude' junto com 'expand'. Use a seleção completa da entidade para expandir relacionamentos.",
                    type="db.invalid_exclude_expand_combination",
                )

            if include and exclude:
                raise ApiError(
                    status_code=400,
                    loc=["query"],
                    msg="Os parâmetros 'include' e 'exclude' não podem ser usados ao mesmo tempo.",
                    type="db.conflict_parameters",
                )

            if cursor_direction not in ("next", "prev"):
                raise ApiError(
                    status_code=422,
                    loc=["query", "cursor_direction"],
                    msg="O parâmetro 'cursor_direction' deve ser 'next' ou 'prev'.",
                    type="pagination.invalid_cursor_direction",
                )

            # Construção da query inicial
            use_custom_columns = False

            if include:
                for attr in include:
                    if attr not in cls.__table__.columns:
                        raise ApiError(
                            status_code=404,
                            loc=["body", attr],
                            msg=f"Atributo '{attr}' não encontrado na tabela '{cls.__tablename__}'.",
                            type="db.attribute_not_found",
                        )
                atributos = [getattr(cls, attr) for attr in include]
                query = select(*atributos)
                use_custom_columns = True

            elif exclude:
                for attr in exclude:
                    if attr not in cls.__table__.columns:
                        raise ApiError(
                            status_code=404,
                            loc=["body", attr],
                            msg=f"Atributo '{attr}' não encontrado na tabela '{cls.__tablename__}'.",
                            type="db.attribute_not_found",
                        )
                atributos = [
                    getattr(cls, col.name)
                    for col in cls.__table__.columns
                    if col.name not in exclude
                ]
                query = select(*atributos)
                use_custom_columns = True

            else:
                query = select(cls)

            # Filtros
            if filters:
                for attribute, value in filters.items():
                    if not isinstance(value, util.FieldQuery):
                        value = util.parse_operator_and_value(str(value))

                    field = getattr(cls, attribute)

                    match value.op.value:
                        case "eq":
                            query = query.filter(field == value.data)
                        case "lk":
                            if isinstance(field.type, String):
                                query = query.filter(field.ilike(f"%{value.data}%"))
                            else:
                                raise ApiError(
                                    status_code=422,
                                    loc=["body", attribute],
                                    msg="Operador 'lk' requer campo do tipo String",
                                    type="db.invalid_operator_type",
                                )
                        case "ne":
                            query = query.filter(field != value.data)
                        case "lt" | "gt" | "le" | "ge":
                            query = query.filter(
                                getattr(field, f"__{value.op.value}__")(value.data)
                            )
                        case "in":
                            if "|" in value.data:
                                lower, upper = value.data.split("|")
                                query = query.filter(field.between(lower, upper))
                            else:
                                query = query.filter(field.in_(value.data.split(",")))
                        case _:
                            raise ApiError(
                                status_code=422,
                                loc=["body", attribute],
                                msg=f"Operador '{value.op.value}' não suportado",
                                type="db.invalid_operator_value",
                            )

            # Ordenação
            if sort_field:
                if not hasattr(cls, sort_field):
                    raise ApiError(
                        status_code=404,
                        loc=["body", "sort_field"],
                        msg=f"Campo '{sort_field}' não encontrado para ordenação",
                        type="db.attribute_not_found",
                    )

                field = getattr(cls, sort_field)
                direction = sort_op.upper() if sort_op else "ASC"
                query = query.order_by(
                    field.asc() if direction == "ASC" else field.desc()
                )

            # Paginação por cursor
            if cursor:
                if not hasattr(cls, cursor_field):
                    raise ApiError(
                        status_code=404,
                        loc=["body", "cursor_field"],
                        msg=f"Campo '{cursor_field}' não encontrado para cursor",
                        type="db.attribute_not_found",
                    )

                cursor_field_attr = getattr(cls, cursor_field)
                query = (
                    query.filter(cursor_field_attr > cursor)
                    if cursor_direction == "next"
                    else query.filter(cursor_field_attr < cursor)
                )

                if not sort_field:
                    query = query.order_by(
                        cursor_field_attr.asc()
                        if cursor_direction == "next"
                        else cursor_field_attr.desc()
                    )

            # Distinct
            if distinct:
                query = query.distinct()

            # Expansão de relacionamentos com estratégia adaptativa
            if expand:
                for relation in expand:
                    rel_name = (
                        relation.value if isinstance(relation, Enum) else relation
                    )

                    if not hasattr(cls, rel_name):
                        raise ApiError(
                            status_code=404,
                            loc=["expand", rel_name],
                            msg=f"O relacionamento '{rel_name}' não existe no modelo '{cls.__name__}'",
                            type="db.expand_relationship_not_found",
                        )

                    rel_attr = getattr(cls, rel_name)
                    prop = getattr(rel_attr, "property", None)

                    if isinstance(prop, RelationshipProperty):
                        direction = prop.direction.name

                        if direction in ("ONETOONE", "MANYTOONE"):
                            # joinedload para relações 1-1 e muitos-para-1
                            query = query.options(joinedload(rel_attr))
                        else:
                            # selectinload para relações muitos-para-muitos ou 1-para-muitos
                            query = query.options(selectinload(rel_attr))
                    else:
                        raise ApiError(
                            status_code=400,
                            loc=["expand", rel_name],
                            msg=f"'{rel_name}' não é uma relação reconhecida para expansão.",
                            type="db.invalid_expand_target",
                        )

            # Contagem total
            total_items = session.query(func.count(cls.id)).scalar()
            subquery = query.subquery()
            total_query = session.query(func.count()).select_from(subquery).scalar()

            # Paginação por offset
            if limit is not None:
                if offset is not None:
                    query = query.offset(offset)
                query = query.limit(limit)

            # Execução
            if count_only:
                data = []
            else:
                result = session.execute(query).unique()
                if use_custom_columns:
                    keys = [col.key for col in query.selected_columns]
                    data = [dict(zip(keys, row)) for row in result.all()]
                else:
                    data = result.scalars().all()

            # Metadados de paginação
            next_cursor = (
                str(getattr(data[-1], cursor_field)) if cursor and data else None
            )
            prev_cursor = (
                str(getattr(data[0], cursor_field)) if cursor and data else None
            )

            next_offset = (
                (offset + limit)
                if offset is not None and (offset + limit) < total_query
                else None
            )
            prev_offset = (offset - limit) if offset and (offset - limit) >= 0 else None
            total_pages = ceil(total_query / limit) if limit else None
            current_page = (offset // limit + 1) if offset and limit else 1

            meta = Meta(
                total_items=total_items,
                total_query=total_query,
                items_per_page=limit,
                current_page=current_page if limit else None,
                total_pages=total_pages,
                next_cursor=next_cursor,
                prev_cursor=prev_cursor,
                next_offset=next_offset,
                prev_offset=prev_offset,
                has_next=next_cursor is not None if cursor else next_offset is not None,
                has_prev=prev_cursor is not None if cursor else prev_offset is not None,
            )

            return ApiSuccess(
                msg=None, meta=meta, data=data if not count_only else None
            )

        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def remove(cls, session: Session, id: UUID) -> ApiSuccess:
        """metodo utilizado para remover um dado da tabela correspondente

        Args:
            id (UUID): Id do dado a ser removido.

        Raises:
            CustomException: 404 em caso de nao encontar dado correspondete ao id remetido.
            CustomException: 400 em caso de um problema durante a exclusão

        Returns:
            str: retorna ok em caso de sucesso.
        """
        try:
            data = session.query(cls).filter_by(id=id).first()
            if not data:
                raise ApiError(
                    status_code=404,
                    loc=["params", "id"],
                    msg=f"{cls.__name__} com ID {id} não encontrado.",
                    type="db.not_found",
                )
            session.delete(data)
            session.commit()
            return ApiSuccess("Registro removido com sucesso!")

        except AssertionError as e:
            session.rollback()
            if "tried to blank-out primary key column" in str(e):
                related_table = str(e).split("'")[
                    3
                ]  # Extrai o nome da tabela relacionada
                raise ApiError(
                    status_code=400,
                    loc=["body", "id"],
                    msg=f"Não é possível remover este {cls.__name__.upper()} pois existem registros em {related_table.replace('_', ' ').split('.')[0].upper()} que dependem dele.",
                    type="db.dependency_error.primary_key_violation",
                    debug=str(e),
                )
            raise ApiError(
                status_code=400,
                loc=["body"],
                msg=f"Regra de dependência violada: {str(e)}",
                type="db.dependency_error",
                debug=str(e),
            )

        except IntegrityError as e:
            session.rollback()
            if "foreign key constraint" in str(e).lower():
                raise ApiError(
                    status_code=400,
                    loc=["body", "id"],
                    msg=f"Não é possível remover este {cls.__name__.upper()} pois ele está sendo referenciado por outros registros.",
                    type="db.integrity_error.foreign_key_violation",
                    debug=str(e),
                )
            raise ApiError(
                status_code=400,
                loc=["body"],
                msg=f"Erro de integridade ao remover {cls.__name__.upper()}",
                type="db.integrity_error",
                debug=str(e),
            )

        except DataError as e:
            session.rollback()
            raise ApiError(
                status_code=400,
                loc=["params", "id"],
                msg="Formato de ID inválido.",
                type="db.data_error",
                debug=str(e),
            )

        except OperationalError as e:
            session.rollback()
            raise ApiError(
                status_code=500,
                loc=["body"],
                msg="Problema de conexão com o banco de dados.",
                type="db.operational_error",
                debug=str(e),
            )

        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def remove_data_and_files(cls, session: Session, id: UUID, files: list) -> str:
        """metodo utilizado para remover um dado da tabela correspondente

        Args:
            id (UUID): Id do dado a ser removido.

        Raises:
            CustomException: 404 em caso de nao encontar dado correspondete ao id remetido.
            CustomException: 400 em caso de um problema durante a exclusão

        Returns:
            str: retorna ok em caso de sucesso.
        """
        try:
            exclude_files = []
            data = session.query(cls).filter_by(id=id).first()
            if not data:
                raise ApiError(
                    status_code=404,
                    loc=["params", "id"],
                    msg=f"{cls.__name__} com ID {id} não encontrado.",
                    type="db.not_found",
                )
            for f in files:
                attr = getattr(data, f)
                if attr:
                    exclude_files.append(attr)

            session.delete(data)
            session.commit()

            for exclude_f in exclude_files:
                util.delete_file(core.settings.UPLOAD_DIR, exclude_f)
            return ApiSuccess(msg="OK")

        except AssertionError as e:
            session.rollback()
            if "tried to blank-out primary key column" in str(e):
                related_table = str(e).split("'")[
                    3
                ]  # Extrai o nome da tabela relacionada
                raise ApiError(
                    status_code=400,
                    loc=["body", "id"],
                    msg=f"Não é possível remover este {cls.__name__.upper()} pois existem registros em {related_table.replace('_', ' ').split('.')[0].upper()} que dependem dele.",
                    type="db.dependency_error.primary_key_violation",
                )
            raise ApiError(
                status_code=400,
                loc=["body"],
                msg=f"Regra de dependência violada: {str(e)}",
                type="db.dependency_error",
            )

        except IntegrityError as e:
            session.rollback()
            if "foreign key constraint" in str(e).lower():
                raise ApiError(
                    status_code=400,
                    loc=["body", "id"],
                    msg=f"Não é possível remover este {cls.__name__.upper()} pois ele está sendo referenciado por outros registros.",
                    type="db.integrity_error.foreign_key_violation",
                )
            raise ApiError(
                status_code=400,
                loc=["body"],
                msg=f"Erro de integridade ao remover {cls.__name__.upper()}",
                type="db.integrity_error",
            )

        except DataError as e:
            session.rollback()
            raise ApiError(
                status_code=400,
                loc=["params", "id"],
                msg="Formato de ID inválido.",
                type="db.data_error",
            )

        except OperationalError as e:
            session.rollback()
            raise ApiError(
                status_code=500,
                loc=["body"],
                msg="Problema de conexão com o banco de dados.",
                type="db.operational_error",
            )

        except Exception as e:
            session.rollback()
            raise e

    def flush(cls, session) -> object:
        """Realiza um flush no banco, um processo que verifica toda a transação mas nao salva, util para teste.

        Returns:
            object: retorna um objeto sqlalchemy
        """
        try:
            session.add(cls)
            session.flush()
            session.refresh(cls)
            return cls
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def update(
        cls,
        session: Session,
        id: UUID,
        response_data: bool = True,
        **json_data: dict[str, Any],
    ) -> Union[ApiSuccess, object]:
        """funçao para atuilizar dados de uma tabela a partir de um dict

        Args:
            id (UUID): UUID do dado a ser atualizado

        Raises:
            CustomException: 404 caso nao haja correspondeica do id a dados nesta tabela

        Returns:
            object: retorna o objeto atualizado
        """
        try:
            data = session.query(cls).filter_by(id=id).first()
            if not data:
                raise ApiError(
                    status_code=404,
                    msg="Dado não encontrado",
                )
            for key, value in json_data.items():
                setattr(data, key, value)
            session.add(data)
            session.commit()
            session.refresh(data)
            if not response_data:
                return {
                    "loc": [data.__class__.__name__],
                    "msg": "Registro Atualizado com sucesso!",
                }
            return data
        except Exception as e:
            session.rollback()
            raise e

    # TODO testar raises da funçao
    @classmethod
    async def update_form(
        cls, session: Session, id: UUID, files: list, response_data: bool = True, **form
    ) -> object:
        """funçao para atuilizar dados de uma tabela a partir de um dict

        Args:
            id (UUID): UUID do dado a ser atualizado

        Raises:
            CustomException: 404 caso nao haja correspondeica do id a dados nesta tabela

        Returns:
            object: retorna o objeto atualizado
        """
        try:
            list_exclude_files = []
            except_exlude_files = []
            data = session.query(cls).filter_by(id=id).first()
            if not data:
                raise ApiError(
                    status_code=404,
                    msg="Dado não encontrado",
                )

            for key, value in form.items():
                if value or str(type(value)) == "<class 'bool'>":
                    for f in files:
                        file_key = next(iter(f.keys()))
                        if key == file_key:
                            list_exclude_files.append(getattr(data, key))
                            filename = await util.save_file(
                                core.settings.UPLOAD_DIR, value, f[key]
                            )
                            except_exlude_files.append(filename)
                            setattr(data, key, filename)
                        else:
                            setattr(data, key, value)
            session.add(data)
            session.commit()
            session.refresh(data)
            if list_exclude_files:
                for filename in list_exclude_files:
                    util.delete_file(core.settings.UPLOAD_DIR, filename)

            if not response_data:
                return {
                    "loc": [str(data.__class__.__name__)],
                    "msg": "Registro Atualizado com sucesso!",
                }
            return data

        except Exception as e:
            if except_exlude_files:
                for filename in except_exlude_files:
                    util.delete_file(core.settings.UPLOAD_DIR, filename)
            raise e

        except:
            if except_exlude_files:
                for filename in except_exlude_files:
                    util.delete_file(core.settings.UPLOAD_DIR, filename)
            raise e

    @classmethod
    def create_form(cls, session: Session, files: dict, **form) -> object:
        try:
            except_exlude_files = []
            data = cls()
            for key, value in form.items():
                if value:
                    for f, tp in files.items():
                        if key == f:
                            filename = util.save_file(
                                core.settings.UPLOAD_DIR, value, tp
                            )
                            except_exlude_files.append(filename)
                            setattr(data, key, filename)
                        else:
                            setattr(data, key, value)
            session.add(data)
            session.commit()
            session.refresh(data)
            return data

        except Exception as e:
            if except_exlude_files:
                for filename in except_exlude_files:
                    util.delete_file(core.settings.UPLOAD_DIR, filename)
            raise e

    @classmethod
    def get(
        cls,
        session: Session,
        attribute: str | None = None,
        value: Any | None = None,
    ) -> object:
        """_summary_

        Args:
            attribute (str): _description_
            value (Any): _description_

        Returns:
            object: _description_
        """

        data = session.query(cls).filter(getattr(cls, attribute) == value).first()

        return data

    @classmethod
    def count(
        cls,
        session: Session,
        attribute: str | None = None,
        value: Any | None = None,
    ) -> int:
        """Retorna a quantidade de registros que correspondem à condição.

        Args:
            attribute (str): Nome do atributo para filtrar.
            value (Any): Valor a ser usado na condição de filtro.

        Returns:
            int: A quantidade de registros que correspondem à condição.
        """
        try:
            query = session.query(cls)

            if attribute is not None and value is not None:
                query = query.filter(getattr(cls, attribute) == value)

            count = query.count()
            return count
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def unique_verify(cls, session: Session, attribute, value):
        try:
            data = session.query(cls).filter(getattr(cls, attribute) == value).first()
            if data:
                raise ApiError(status_code=422, msg=f"{value} ja existe")
            return value
        except Exception as e:
            session.rollback()
            raise e
