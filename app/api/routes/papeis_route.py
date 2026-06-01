from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.papeis_schema import (
    QueryPapeisDep,
    GetPapeis,
    PostPapeis,
    PatchPapeis,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.papeis import (
    get_papeis,
    create_papeis,
    update_papeis,
    delete_papeis,
)


router = APIRouter(prefix="/papeis", tags=["Papeis"])


@router.get(
    "/",
    response_model=ApiSuccess[GetPapeis],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Papeis",
    operation_id="ler_papeis",
)
def papeis(
    query: QueryPapeisDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetPapeis]:
    return get_papeis(session, query)


@router.post(
    "/",
    summary="Criar Papeis",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_papeis",
    response_model_exclude_none=True,
)
def papeis(
    json_data: PostPapeis,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_papeis(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Papeis",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_papeis",
    response_model_exclude_none=True,
)
def papeis(
    session: sessionDep,
    json_data: PatchPapeis,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_papeis(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Papeis",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_papeis",
    response_model_exclude_none=True,
)
def papeis(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_papeis(session, id)
