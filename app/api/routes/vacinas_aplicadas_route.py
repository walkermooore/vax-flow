from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.vacinas_aplicadas_schema import (
    QueryVacinasAplicadasDep,
    GetVacinasAplicadas,
    PostVacinasAplicadas,
    PatchVacinasAplicadas,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.vacinas_aplicadas import (
    get_vacinas_aplicadas,
    create_vacinas_aplicadas,
    update_vacinas_aplicadas,
    delete_vacinas_aplicadas,
)


router = APIRouter(prefix="/vacinas-aplicadas", tags=["VacinasAplicadas"])


@router.get(
    "/",
    response_model=ApiSuccess[GetVacinasAplicadas],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Vacinas Aplicadas",
    operation_id="ler_vacinas_aplicadas",
)
def vacinas_aplicadas(
    query: QueryVacinasAplicadasDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetVacinasAplicadas]:
    return get_vacinas_aplicadas(session, query)


@router.post(
    "/",
    summary="Criar Vacinas Aplicadas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_vacinas_aplicadas",
    response_model_exclude_none=True,
)
def vacinas_aplicadas(
    json_data: PostVacinasAplicadas,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_vacinas_aplicadas(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Vacinas Aplicadas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_vacinas_aplicadas",
    response_model_exclude_none=True,
)
def vacinas_aplicadas(
    session: sessionDep,
    json_data: PatchVacinasAplicadas,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_vacinas_aplicadas(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Vacinas Aplicadas",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_vacinas_aplicadas",
    response_model_exclude_none=True,
)
def vacinas_aplicadas(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_vacinas_aplicadas(session, id)
