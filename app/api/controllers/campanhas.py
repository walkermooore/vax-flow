from pydantic.types import UUID4

from app.models import Campanhas
from app.schema.campanhas_schema import PostCampanhas, PatchCampanhas, QueryCampanhasDep, GetCampanhas

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_campanhas",
    "create_campanhas",
    "update_campanhas",
    "delete_campanhas",
]


def get_campanhas(
    session: Session,
    query: QueryCampanhasDep
) -> ApiSuccess[GetCampanhas]:
    return Campanhas.query_params(session, **query.__dict__)


def create_campanhas(
    session: Session,
    json_data: PostCampanhas
)-> ApiSuccess[None]:
    data = Campanhas(**json_data.model_dump())
    return data.create(session)


def update_campanhas(
    session: Session,
    id: UUID4,
    json_data: PatchCampanhas
) -> ApiSuccess[None]:
    return Campanhas.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_campanhas(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return Campanhas.remove(session, id)