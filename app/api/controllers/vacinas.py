from pydantic.types import UUID4

from app.models import Vacinas
from app.schema.vacinas_schema import PostVacinas, PatchVacinas, QueryVacinasDep, GetVacinas

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_vacinas",
    "create_vacinas",
    "update_vacinas",
    "delete_vacinas",
]


def get_vacinas(
    session: Session,
    query: QueryVacinasDep
) -> ApiSuccess[GetVacinas]:
    return Vacinas.query_params(session, **query.__dict__)


def create_vacinas(
    session: Session,
    json_data: PostVacinas
)-> ApiSuccess[None]:
    data = Vacinas(**json_data.model_dump())
    return data.create(session)


def update_vacinas(
    session: Session,
    id: UUID4,
    json_data: PatchVacinas
) -> ApiSuccess[None]:
    return Vacinas.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_vacinas(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return Vacinas.remove(session, id)