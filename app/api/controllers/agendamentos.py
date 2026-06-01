from pydantic.types import UUID4

from app.models import Agendamentos
from app.schema.agendamentos_schema import PostAgendamentos, PatchAgendamentos, QueryAgendamentosDep, GetAgendamentos

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_agendamentos",
    "create_agendamentos",
    "update_agendamentos",
    "delete_agendamentos",
]


def get_agendamentos(
    session: Session,
    query: QueryAgendamentosDep
) -> ApiSuccess[GetAgendamentos]:
    return Agendamentos.query_params(session, **query.__dict__)


def create_agendamentos(
    session: Session,
    json_data: PostAgendamentos
)-> ApiSuccess[None]:
    data = Agendamentos(**json_data.model_dump())
    return data.create(session)


def update_agendamentos(
    session: Session,
    id: UUID4,
    json_data: PatchAgendamentos
) -> ApiSuccess[None]:
    return Agendamentos.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_agendamentos(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return Agendamentos.remove(session, id)