from pydantic.types import UUID4

from app.models import UsuariosFuncionalidades
from app.schema.usuarios_funcionalidades_schema import PostUsuariosFuncionalidades, PatchUsuariosFuncionalidades, QueryUsuariosFuncionalidadesDep, GetUsuariosFuncionalidades

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_usuarios_funcionalidades",
    "create_usuarios_funcionalidades",
    "update_usuarios_funcionalidades",
    "delete_usuarios_funcionalidades",
]


def get_usuarios_funcionalidades(
    session: Session,
    query: QueryUsuariosFuncionalidadesDep
) -> ApiSuccess[GetUsuariosFuncionalidades]:
    return UsuariosFuncionalidades.query_params(session, **query.__dict__)


def create_usuarios_funcionalidades(
    session: Session,
    json_data: PostUsuariosFuncionalidades
)-> ApiSuccess[None]:
    data = UsuariosFuncionalidades(**json_data.model_dump())
    return data.create(session)


def update_usuarios_funcionalidades(
    session: Session,
    id: UUID4,
    json_data: PatchUsuariosFuncionalidades
) -> ApiSuccess[None]:
    return UsuariosFuncionalidades.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_usuarios_funcionalidades(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return UsuariosFuncionalidades.remove(session, id)