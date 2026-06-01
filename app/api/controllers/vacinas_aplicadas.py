from pydantic.types import UUID4

from app.models import VacinasAplicadas
from app.schema.vacinas_aplicadas_schema import PostVacinasAplicadas, PatchVacinasAplicadas, QueryVacinasAplicadasDep, GetVacinasAplicadas

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_vacinas_aplicadas",
    "create_vacinas_aplicadas",
    "update_vacinas_aplicadas",
    "delete_vacinas_aplicadas",
]


def get_vacinas_aplicadas(
    session: Session,
    query: QueryVacinasAplicadasDep
) -> ApiSuccess[GetVacinasAplicadas]:
    return VacinasAplicadas.query_params(session, **query.__dict__)


def create_vacinas_aplicadas(
    session: Session,
    json_data: PostVacinasAplicadas
)-> ApiSuccess[None]:
    data = VacinasAplicadas(**json_data.model_dump())
    return data.create(session)


def update_vacinas_aplicadas(
    session: Session,
    id: UUID4,
    json_data: PatchVacinasAplicadas
) -> ApiSuccess[None]:
    return VacinasAplicadas.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_vacinas_aplicadas(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return VacinasAplicadas.remove(session, id)