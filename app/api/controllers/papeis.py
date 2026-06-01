from pydantic.types import UUID4

from app.models import Papeis
from app.schema.papeis_schema import PostPapeis, PatchPapeis, QueryPapeisDep, GetPapeis

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_papeis",
    "create_papeis",
    "update_papeis",
    "delete_papeis",
]


def get_papeis(
    session: Session,
    query: QueryPapeisDep
) -> ApiSuccess[GetPapeis]:
    return Papeis.query_params(session, **query.__dict__)


def create_papeis(
    session: Session,
    json_data: PostPapeis
)-> ApiSuccess[None]:
    data = Papeis(**json_data.model_dump())
    return data.create(session)


def update_papeis(
    session: Session,
    id: UUID4,
    json_data: PatchPapeis
) -> ApiSuccess[None]:
    return Papeis.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_papeis(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return Papeis.remove(session, id)