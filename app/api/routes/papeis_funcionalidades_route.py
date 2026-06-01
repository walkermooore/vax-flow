from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.papeis_funcionalidades_schema import (
    QueryPapeisFuncionalidadesDep,
    GetPapeisFuncionalidades,
    PostPapeisFuncionalidades,
    PatchPapeisFuncionalidades,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.papeis_funcionalidades import (
    get_papeis_funcionalidades,
    create_papeis_funcionalidades,
    update_papeis_funcionalidades,
    delete_papeis_funcionalidades,
)


router = APIRouter(prefix="/papeis-funcionalidades", tags=["PapeisFuncionalidades"])


@router.get(
    "/",
    response_model=ApiSuccess[GetPapeisFuncionalidades],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Papeis Funcionalidades",
    operation_id="ler_papeis_funcionalidades",
)
def papeis_funcionalidades(
    query: QueryPapeisFuncionalidadesDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetPapeisFuncionalidades]:
    return get_papeis_funcionalidades(session, query)


@router.post(
    "/",
    summary="Criar Papeis Funcionalidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_papeis_funcionalidades",
    response_model_exclude_none=True,
)
def papeis_funcionalidades(
    json_data: PostPapeisFuncionalidades,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_papeis_funcionalidades(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Papeis Funcionalidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_papeis_funcionalidades",
    response_model_exclude_none=True,
)
def papeis_funcionalidades(
    session: sessionDep,
    json_data: PatchPapeisFuncionalidades,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_papeis_funcionalidades(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Papeis Funcionalidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_papeis_funcionalidades",
    response_model_exclude_none=True,
)
def papeis_funcionalidades(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_papeis_funcionalidades(session, id)
