from pydantic.types import UUID4

from app.models import CampanhasUnidades
from app.schema.campanhas_unidades_schema import PostCampanhasUnidades, PatchCampanhasUnidades, QueryCampanhasUnidadesDep, GetCampanhasUnidades

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_campanhas_unidades",
    "create_campanhas_unidades",
    "update_campanhas_unidades",
    "delete_campanhas_unidades",
]


def get_campanhas_unidades(
    session: Session,
    query: QueryCampanhasUnidadesDep
) -> ApiSuccess[GetCampanhasUnidades]:
    return CampanhasUnidades.query_params(session, **query.__dict__)


def create_campanhas_unidades(
    session: Session,
    json_data: PostCampanhasUnidades
)-> ApiSuccess[None]:
    data = CampanhasUnidades(**json_data.model_dump())
    return data.create(session)


def update_campanhas_unidades(
    session: Session,
    id: UUID4,
    json_data: PatchCampanhasUnidades
) -> ApiSuccess[None]:
    return CampanhasUnidades.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_campanhas_unidades(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return CampanhasUnidades.remove(session, id)