from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.lotes_schema import (
    QueryLotesDep,
    GetLotes,
    PostLotes,
    PatchLotes,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.lotes import (
    get_lotes,
    create_lotes,
    update_lotes,
    delete_lotes,
)


router = APIRouter(prefix="/lotes", tags=["Lotes"])


@router.get(
    "/",
    response_model=ApiSuccess[GetLotes],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Lotes",
    operation_id="ler_lotes",
)
def lotes(
    query: QueryLotesDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetLotes]:
    return get_lotes(session, query)


@router.post(
    "/",
    summary="Criar Lotes",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_lotes",
    response_model_exclude_none=True,
)
def lotes(
    json_data: PostLotes,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_lotes(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Lotes",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_lotes",
    response_model_exclude_none=True,
)
def lotes(
    session: sessionDep,
    json_data: PatchLotes,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_lotes(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Lotes",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_lotes",
    response_model_exclude_none=True,
)
def lotes(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_lotes(session, id)
