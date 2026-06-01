from pydantic.types import UUID4

from app.models import AgendasVacinas
from app.schema.agendas_vacinas_schema import PostAgendasVacinas, PatchAgendasVacinas, QueryAgendasVacinasDep, GetAgendasVacinas

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_agendas_vacinas",
    "create_agendas_vacinas",
    "update_agendas_vacinas",
    "delete_agendas_vacinas",
]


def get_agendas_vacinas(
    session: Session,
    query: QueryAgendasVacinasDep
) -> ApiSuccess[GetAgendasVacinas]:
    return AgendasVacinas.query_params(session, **query.__dict__)


def create_agendas_vacinas(
    session: Session,
    json_data: PostAgendasVacinas
)-> ApiSuccess[None]:
    data = AgendasVacinas(**json_data.model_dump())
    return data.create(session)


def update_agendas_vacinas(
    session: Session,
    id: UUID4,
    json_data: PatchAgendasVacinas
) -> ApiSuccess[None]:
    return AgendasVacinas.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_agendas_vacinas(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return AgendasVacinas.remove(session, id)