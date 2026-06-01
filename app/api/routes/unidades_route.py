from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.unidades_schema import (
    QueryUnidadesDep,
    GetUnidades,
    PostUnidades,
    PatchUnidades,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.unidades import (
    get_unidades,
    create_unidades,
    update_unidades,
    delete_unidades,
)


router = APIRouter(prefix="/unidades", tags=["Unidades"])


@router.get(
    "/",
    response_model=ApiSuccess[GetUnidades],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Unidades",
    operation_id="ler_unidades",
)
def unidades(
    query: QueryUnidadesDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetUnidades]:
    return get_unidades(session, query)


@router.post(
    "/",
    summary="Criar Unidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_unidades",
    response_model_exclude_none=True,
)
def unidades(
    json_data: PostUnidades,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_unidades(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Unidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_unidades",
    response_model_exclude_none=True,
)
def unidades(
    session: sessionDep,
    json_data: PatchUnidades,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_unidades(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Unidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_unidades",
    response_model_exclude_none=True,
)
def unidades(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_unidades(session, id)
