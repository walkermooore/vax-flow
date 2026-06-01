from pydantic.types import UUID4

from app.models import PapeisFuncionalidades
from app.schema.papeis_funcionalidades_schema import PostPapeisFuncionalidades, PatchPapeisFuncionalidades, QueryPapeisFuncionalidadesDep, GetPapeisFuncionalidades

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_papeis_funcionalidades",
    "create_papeis_funcionalidades",
    "update_papeis_funcionalidades",
    "delete_papeis_funcionalidades",
]


def get_papeis_funcionalidades(
    session: Session,
    query: QueryPapeisFuncionalidadesDep
) -> ApiSuccess[GetPapeisFuncionalidades]:
    return PapeisFuncionalidades.query_params(session, **query.__dict__)


def create_papeis_funcionalidades(
    session: Session,
    json_data: PostPapeisFuncionalidades
)-> ApiSuccess[None]:
    data = PapeisFuncionalidades(**json_data.model_dump())
    return data.create(session)


def update_papeis_funcionalidades(
    session: Session,
    id: UUID4,
    json_data: PatchPapeisFuncionalidades
) -> ApiSuccess[None]:
    return PapeisFuncionalidades.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_papeis_funcionalidades(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return PapeisFuncionalidades.remove(session, id)