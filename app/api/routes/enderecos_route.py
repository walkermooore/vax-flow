from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.enderecos_schema import (
    QueryEnderecosDep,
    GetEnderecos,
    PostEnderecos,
    PatchEnderecos,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.enderecos import (
    get_enderecos,
    create_enderecos,
    update_enderecos,
    delete_enderecos,
)


router = APIRouter(prefix="/enderecos", tags=["Enderecos"])


@router.get(
    "/",
    response_model=ApiSuccess[GetEnderecos],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Enderecos",
    operation_id="ler_enderecos",
)
def enderecos(
    query: QueryEnderecosDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetEnderecos]:
    return get_enderecos(session, query)


@router.post(
    "/",
    summary="Criar Enderecos",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_enderecos",
    response_model_exclude_none=True,
)
def enderecos(
    json_data: PostEnderecos,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_enderecos(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Enderecos",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_enderecos",
    response_model_exclude_none=True,
)
def enderecos(
    session: sessionDep,
    json_data: PatchEnderecos,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_enderecos(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Enderecos",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_enderecos",
    response_model_exclude_none=True,
)
def enderecos(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_enderecos(session, id)
