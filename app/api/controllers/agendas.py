from pydantic.types import UUID4

from app.models import Agendas
from app.schema.agendas_schema import PostAgendas, PatchAgendas, QueryAgendasDep, GetAgendas

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_agendas",
    "create_agendas",
    "update_agendas",
    "delete_agendas",
]


def get_agendas(
    session: Session,
    query: QueryAgendasDep
) -> ApiSuccess[GetAgendas]:
    return Agendas.query_params(session, **query.__dict__)


def create_agendas(
    session: Session,
    json_data: PostAgendas
)-> ApiSuccess[None]:
    data = Agendas(**json_data.model_dump())
    return data.create(session)


def update_agendas(
    session: Session,
    id: UUID4,
    json_data: PatchAgendas
) -> ApiSuccess[None]:
    return Agendas.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_agendas(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return Agendas.remove(session, id)