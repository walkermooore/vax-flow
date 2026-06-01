from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.agendamentos_schema import (
    QueryAgendamentosDep,
    GetAgendamentos,
    PostAgendamentos,
    PatchAgendamentos,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.agendamentos import (
    get_agendamentos,
    create_agendamentos,
    update_agendamentos,
    delete_agendamentos,
)


router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])


@router.get(
    "/",
    response_model=ApiSuccess[GetAgendamentos],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Agendamentos",
    operation_id="ler_agendamentos",
)
def agendamentos(
    query: QueryAgendamentosDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetAgendamentos]:
    return get_agendamentos(session, query)


@router.post(
    "/",
    summary="Criar Agendamentos",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_agendamentos",
    response_model_exclude_none=True,
)
def agendamentos(
    json_data: PostAgendamentos,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_agendamentos(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Agendamentos",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_agendamentos",
    response_model_exclude_none=True,
)
def agendamentos(
    session: sessionDep,
    json_data: PatchAgendamentos,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_agendamentos(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Agendamentos",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_agendamentos",
    response_model_exclude_none=True,
)
def agendamentos(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_agendamentos(session, id)
