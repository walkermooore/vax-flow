from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.agendas_vacinas_schema import (
    QueryAgendasVacinasDep,
    GetAgendasVacinas,
    PostAgendasVacinas,
    PatchAgendasVacinas,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.agendas_vacinas import (
    get_agendas_vacinas,
    create_agendas_vacinas,
    update_agendas_vacinas,
    delete_agendas_vacinas,
)


router = APIRouter(prefix="/agendas-vacinas", tags=["AgendasVacinas"])


@router.get(
    "/",
    response_model=ApiSuccess[GetAgendasVacinas],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Agendas Vacinas",
    operation_id="ler_agendas_vacinas",
)
def agendas_vacinas(
    query: QueryAgendasVacinasDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetAgendasVacinas]:
    return get_agendas_vacinas(session, query)


@router.post(
    "/",
    summary="Criar Agendas Vacinas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_agendas_vacinas",
    response_model_exclude_none=True,
)
def agendas_vacinas(
    json_data: PostAgendasVacinas,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_agendas_vacinas(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Agendas Vacinas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_agendas_vacinas",
    response_model_exclude_none=True,
)
def agendas_vacinas(
    session: sessionDep,
    json_data: PatchAgendasVacinas,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_agendas_vacinas(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Agendas Vacinas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_agendas_vacinas",
    response_model_exclude_none=True,
)
def agendas_vacinas(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_agendas_vacinas(session, id)
