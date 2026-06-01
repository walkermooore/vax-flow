from pydantic.types import UUID4

from app.models import Enderecos
from app.schema.enderecos_schema import PostEnderecos, PatchEnderecos, QueryEnderecosDep, GetEnderecos

from sqlalchemy.orm import Session
from app.core import ApiSuccess


__all__ = [
    "get_enderecos",
    "create_enderecos",
    "update_enderecos",
    "delete_enderecos",
]


def get_enderecos(
    session: Session,
    query: QueryEnderecosDep
) -> ApiSuccess[GetEnderecos]:
    return Enderecos.query_params(session, **query.__dict__)


def create_enderecos(
    session: Session,
    json_data: PostEnderecos
)-> ApiSuccess[None]:
    data = Enderecos(**json_data.model_dump())
    return data.create(session)


def update_enderecos(
    session: Session,
    id: UUID4,
    json_data: PatchEnderecos
) -> ApiSuccess[None]:
    return Enderecos.update(session,
        id,
        **json_data.model_dump(exclude_unset=True)
    )


def delete_enderecos(
    session: Session,
    id: UUID4
) -> ApiSuccess[None]:
    return Enderecos.remove(session, id)