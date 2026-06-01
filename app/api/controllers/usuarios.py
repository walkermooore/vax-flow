from pydantic.types import UUID4

from app.models import Usuarios
from app.schema.usuarios_schema import PostUsuarios, PatchUsuarios, QueryUsuariosDep, GetUsuarios

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_usuarios",
    "create_usuarios",
    "update_usuarios",
    "delete_usuarios",
]


def get_usuarios(
    session: Session,
    query: QueryUsuariosDep
) -> ApiSuccess[GetUsuarios]:
    return Usuarios.query_params(session, **query.__dict__)


def create_usuarios(
    session: Session,
    json_data: PostUsuarios
)-> ApiSuccess[None]:
    data = Usuarios(**json_data.model_dump())
    return data.create(session)


def update_usuarios(
    session: Session,
    id: UUID4,
    json_data: PatchUsuarios
) -> ApiSuccess[None]:
    return Usuarios.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_usuarios(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return Usuarios.remove(session, id)