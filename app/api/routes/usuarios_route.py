from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.usuarios_schema import (
    QueryUsuariosDep,
    GetUsuarios,
    PostUsuarios,
    PatchUsuarios,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.usuarios import (
    get_usuarios,
    create_usuarios,
    update_usuarios,
    delete_usuarios,
)


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get(
    "/",
    response_model=ApiSuccess[GetUsuarios],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Usuarios",
    operation_id="ler_usuarios",
)
def usuarios(
    query: QueryUsuariosDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetUsuarios]:
    return get_usuarios(session, query)


@router.post(
    "/",
    summary="Criar Usuarios",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_usuarios",
    response_model_exclude_none=True,
)
def usuarios(
    json_data: PostUsuarios,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_usuarios(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Usuarios",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_usuarios",
    response_model_exclude_none=True,
)
def usuarios(
    session: sessionDep,
    json_data: PatchUsuarios,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_usuarios(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Usuarios",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_usuarios",
    response_model_exclude_none=True,
)
def usuarios(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_usuarios(session, id)
