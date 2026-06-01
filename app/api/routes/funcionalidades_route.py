from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.funcionalidades_schema import (
    QueryFuncionalidadesDep,
    GetFuncionalidades,
    PostFuncionalidades,
    PatchFuncionalidades,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.funcionalidades import (
    get_funcionalidades,
    create_funcionalidades,
    update_funcionalidades,
    delete_funcionalidades,
)


router = APIRouter(prefix="/funcionalidades", tags=["Funcionalidades"])


@router.get(
    "/",
    response_model=ApiSuccess[GetFuncionalidades],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Funcionalidades",
    operation_id="ler_funcionalidades",
)
def funcionalidades(
    query: QueryFuncionalidadesDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetFuncionalidades]:
    return get_funcionalidades(session, query)


@router.post(
    "/",
    summary="Criar Funcionalidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_funcionalidades",
    response_model_exclude_none=True,
)
def funcionalidades(
    json_data: PostFuncionalidades,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_funcionalidades(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Funcionalidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_funcionalidades",
    response_model_exclude_none=True,
)
def funcionalidades(
    session: sessionDep,
    json_data: PatchFuncionalidades,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_funcionalidades(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Funcionalidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_funcionalidades",
    response_model_exclude_none=True,
)
def funcionalidades(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_funcionalidades(session, id)
