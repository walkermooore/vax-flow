from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.campanhas_schema import (
    QueryCampanhasDep,
    GetCampanhas,
    PostCampanhas,
    PatchCampanhas,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.campanhas import (
    get_campanhas,
    create_campanhas,
    update_campanhas,
    delete_campanhas,
)


router = APIRouter(prefix="/campanhas", tags=["Campanhas"])


@router.get(
    "/",
    response_model=ApiSuccess[GetCampanhas],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Campanhas",
    operation_id="ler_campanhas",
)
def campanhas(
    query: QueryCampanhasDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetCampanhas]:
    return get_campanhas(session, query)


@router.post(
    "/",
    summary="Criar Campanhas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_campanhas",
    response_model_exclude_none=True,
)
def campanhas(
    json_data: PostCampanhas,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_campanhas(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Campanhas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_campanhas",
    response_model_exclude_none=True,
)
def campanhas(
    session: sessionDep,
    json_data: PatchCampanhas,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_campanhas(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Campanhas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_campanhas",
    response_model_exclude_none=True,
)
def campanhas(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_campanhas(session, id)
