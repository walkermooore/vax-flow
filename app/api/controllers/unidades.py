from pydantic.types import UUID4

from app.models import Unidades
from app.schema.unidades_schema import PostUnidades, PatchUnidades, QueryUnidadesDep, GetUnidades

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_unidades",
    "create_unidades",
    "update_unidades",
    "delete_unidades",
]


def get_unidades(
    session: Session,
    query: QueryUnidadesDep
) -> ApiSuccess[GetUnidades]:
    return Unidades.query_params(session, **query.__dict__)


def create_unidades(
    session: Session,
    json_data: PostUnidades
)-> ApiSuccess[None]:
    data = Unidades(**json_data.model_dump())
    return data.create(session)


def update_unidades(
    session: Session,
    id: UUID4,
    json_data: PatchUnidades
) -> ApiSuccess[None]:
    return Unidades.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_unidades(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return Unidades.remove(session, id)