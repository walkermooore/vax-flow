from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.vacinas_schema import (
    QueryVacinasDep,
    GetVacinas,
    PostVacinas,
    PatchVacinas,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.vacinas import (
    get_vacinas,
    create_vacinas,
    update_vacinas,
    delete_vacinas,
)


router = APIRouter(prefix="/vacinas", tags=["Vacinas"])


@router.get(
    "/",
    response_model=ApiSuccess[GetVacinas],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Vacinas",
    operation_id="ler_vacinas",
)
def vacinas(
    query: QueryVacinasDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetVacinas]:
    return get_vacinas(session, query)


@router.post(
    "/",
    summary="Criar Vacinas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_vacinas",
    response_model_exclude_none=True,
)
def vacinas(
    json_data: PostVacinas,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_vacinas(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Vacinas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_vacinas",
    response_model_exclude_none=True,
)
def vacinas(
    session: sessionDep,
    json_data: PatchVacinas,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_vacinas(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Vacinas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_vacinas",
    response_model_exclude_none=True,
)
def vacinas(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_vacinas(session, id)
