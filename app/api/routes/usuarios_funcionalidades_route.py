from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from pydantic.types import UUID4

from app.auth import Key
from app.schema.usuarios_funcionalidades_schema import (
    QueryUsuariosFuncionalidadesDep,
    GetUsuariosFuncionalidades,
    PostUsuariosFuncionalidades,
    PatchUsuariosFuncionalidades,
)

from app.core import ApiSuccess, RESPONSE
from app.db.session import sessionDep
from app.api.controllers.usuarios_funcionalidades import (
    get_usuarios_funcionalidades,
    create_usuarios_funcionalidades,
    update_usuarios_funcionalidades,
    delete_usuarios_funcionalidades,
)


router = APIRouter(prefix="/usuarios-funcionalidades", tags=["UsuariosFuncionalidades"])


@router.get(
    "/",
    response_model=ApiSuccess[GetUsuariosFuncionalidades],
    responses=RESPONSE,
    response_model_exclude_none=True,
    summary="Ler Usuarios Funcionalidades",
    operation_id="ler_usuarios_funcionalidades",
)
def usuarios_funcionalidades(
    query: QueryUsuariosFuncionalidadesDep,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[GetUsuariosFuncionalidades]:
    return get_usuarios_funcionalidades(session, query)


@router.post(
    "/",
    summary="Criar Usuarios Funcionalidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    status_code=201,
    operation_id="criar_usuarios_funcionalidades",
    response_model_exclude_none=True,
)
def usuarios_funcionalidades(
    json_data: PostUsuariosFuncionalidades,
    session: sessionDep,
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return create_usuarios_funcionalidades(session, json_data)


@router.patch(
    "/{id}",
    summary="Atualizar Usuarios Funcionalidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="atualizar_usuarios_funcionalidades",
    response_model_exclude_none=True,
)
def usuarios_funcionalidades(
    session: sessionDep,
    json_data: PatchUsuariosFuncionalidades,
    id: UUID4 = Path(..., description="ID dado a ser atualizado"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return update_usuarios_funcionalidades(session, id, json_data)


@router.delete(
    "/{id}",
    summary="Remover Usuarios Funcionalidades",
    response_model=ApiSuccess[None],
    responses=RESPONSE,
    operation_id="remover_usuarios_funcionalidades",
    response_model_exclude_none=True,
)
def usuarios_funcionalidades(
    session: sessionDep,
    id: UUID4 = Path(..., description="ID dado a ser removido"),
    current_user: str = Depends(Key.closed),
) -> ApiSuccess[None]:
    return delete_usuarios_funcionalidades(session, id)
