from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.agendas_schema import (
    QueryAgendasDep,
    GetAgendas,
    PostAgendas,
    PatchAgendas,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.agendas import (
    get_agendas,
    create_agendas,
    update_agendas,
    delete_agendas,
)


router = APIRouter(prefix="/agendas", tags=["Agendas"])


@router.get(
    "/",
    response_model=ApiSuccess[GetAgendas],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Agendas",
    operation_id="ler_agendas",
)
def agendas(
    query: QueryAgendasDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetAgendas]:
    return get_agendas(session, query)


@router.post(
    "/",
    summary="Criar Agendas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_agendas",
    response_model_exclude_none=True,
)
def agendas(
    json_data: PostAgendas,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_agendas(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Agendas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_agendas",
    response_model_exclude_none=True,
)
def agendas(
    session: sessionDep,
    json_data: PatchAgendas,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_agendas(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Agendas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_agendas",
    response_model_exclude_none=True,
)
def agendas(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_agendas(session, id)
