from pydantic.types import UUID4

from app.models import Lotes
from app.schema.lotes_schema import PostLotes, PatchLotes, QueryLotesDep, GetLotes

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_lotes",
    "create_lotes",
    "update_lotes",
    "delete_lotes",
]


def get_lotes(
    session: Session,
    query: QueryLotesDep
) -> ApiSuccess[GetLotes]:
    return Lotes.query_params(session, **query.__dict__)


def create_lotes(
    session: Session,
    json_data: PostLotes
)-> ApiSuccess[None]:
    data = Lotes(**json_data.model_dump())
    return data.create(session)


def update_lotes(
    session: Session,
    id: UUID4,
    json_data: PatchLotes
) -> ApiSuccess[None]:
    return Lotes.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_lotes(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return Lotes.remove(session, id)