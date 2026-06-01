from pydantic.types import UUID4

from app.models import Funcionalidades
from app.schema.funcionalidades_schema import PostFuncionalidades, PatchFuncionalidades, QueryFuncionalidadesDep, GetFuncionalidades

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_funcionalidades",
    "create_funcionalidades",
    "update_funcionalidades",
    "delete_funcionalidades",
]


def get_funcionalidades(
    session: Session,
    query: QueryFuncionalidadesDep
) -> ApiSuccess[GetFuncionalidades]:
    return Funcionalidades.query_params(session, **query.__dict__)


def create_funcionalidades(
    session: Session,
    json_data: PostFuncionalidades
)-> ApiSuccess[None]:
    data = Funcionalidades(**json_data.model_dump())
    return data.create(session)


def update_funcionalidades(
    session: Session,
    id: UUID4,
    json_data: PatchFuncionalidades
) -> ApiSuccess[None]:
    return Funcionalidades.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_funcionalidades(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return Funcionalidades.remove(session, id)