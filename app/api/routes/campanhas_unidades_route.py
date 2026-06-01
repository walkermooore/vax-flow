from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.campanhas_unidades_schema import (
    QueryCampanhasUnidadesDep,
    GetCampanhasUnidades,
    PostCampanhasUnidades,
    PatchCampanhasUnidades,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.campanhas_unidades import (
    get_campanhas_unidades,
    create_campanhas_unidades,
    update_campanhas_unidades,
    delete_campanhas_unidades,
)


router = APIRouter(prefix="/campanhas-unidades", tags=["CampanhasUnidades"])


@router.get(
    "/",
    response_model=ApiSuccess[GetCampanhasUnidades],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Campanhas Unidades",
    operation_id="ler_campanhas_unidades",
)
def campanhas_unidades(
    query: QueryCampanhasUnidadesDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetCampanhasUnidades]:
    return get_campanhas_unidades(session, query)


@router.post(
    "/",
    summary="Criar Campanhas Unidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_campanhas_unidades",
    response_model_exclude_none=True,
)
def campanhas_unidades(
    json_data: PostCampanhasUnidades,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_campanhas_unidades(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Campanhas Unidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_campanhas_unidades",
    response_model_exclude_none=True,
)
def campanhas_unidades(
    session: sessionDep,
    json_data: PatchCampanhasUnidades,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_campanhas_unidades(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Campanhas Unidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_campanhas_unidades",
    response_model_exclude_none=True,
)
def campanhas_unidades(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_campanhas_unidades(session, id)
