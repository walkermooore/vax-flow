import logging
from typing import Any, Coroutine, Dict, Generic, TypeVar, Union

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing_extensions import Protocol, TypedDict

# Configuração básica do logger (ajuste conforme necessário)
logger = logging.getLogger(__name__)


T = TypeVar("T")


class Meta(BaseModel):
    """Metadados para operações"""

    total_items: int = Field(0, description="Total de itens disponíveis")
    total_query: int = Field(0, description="Total de itens retornados na consulta")
    items_per_page: int | None = Field(10, description="Quantidade de itens por página")

    # Paginação numérica
    current_page: int | None = Field(None, description="Página atual")
    total_pages: int | None = Field(None, description="Total de páginas")

    # Paginação por cursor
    next_cursor: str | None = Field(None, description="Cursor para próxima página")
    prev_cursor: str | None = Field(None, description="Cursor para página anterior")

    # Paginação por offset
    next_offset: int | None = Field(None, description="Offset para próxima página")
    prev_offset: int | None = Field(None, description="Offset para página anterior")

    # Controles de navegação
    has_next: bool | None = Field(
        None, description="Existem mais itens após os retornados"
    )
    has_prev: bool | None = Field(
        None, description="Existem itens antes dos retornados"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "total_items": 150,
                "total_items": 75,
                "items_per_page": 10,
                "current_page": 1,
                "total_pages": 15,
                "next_cursor": "abc123",
                "prev_cursor": "zyx987",
                "next_offset": 10,
                "prev_offset": 0,
                "has_next": True,
                "has_prev": True,
            }
        }
    }


class ApiSuccess(
    BaseModel,
    Generic[T],
):
    msg: str | None = "Success"
    meta: Meta | None = None
    data: list[T] | None = Field(
        None, description="Lista de itens do tipo especificado"
    )

    model_config = {"from_attributes": True}

    def __init__(
        self,
        msg: str | None = None,
        *,
        meta: Meta | None = None,
        data: list[T] | None = None,
        **kwargs: Any,
    ):
        if msg is not None and "msg" not in kwargs:
            kwargs["msg"] = msg
        if meta is not None and "meta" not in kwargs:
            kwargs["meta"] = meta
        if data is not None and "data" not in kwargs:
            kwargs["data"] = data
        super().__init__(**kwargs)


# Modelo para detalhes individuais de erro
class Detail(BaseModel):
    loc: list[Union[str, int]] | None = Field(
        ["global"], description="Lista de localizações onde o erro ocorreu"
    )
    msg: str = Field(..., description="Mensagem descritiva do erro")
    type: str | None = Field(None, description="Tipo/categoria do erro")
    debug: str | None = Field(
        None, description="Detalhes adicionais do erro retornados em desenvolvimento"
    )


class ErrorSchema(BaseModel):
    detail: list[Detail] = Field(
        ..., description="Lista de detalhes dos erros ocorridos"
    )


# Definindo o tipo para o dicionário RESPONSE
ResponseModels = Dict[Union[int, str], Dict[str, Any]]


# Protocolo para tipagem dos handlers de exceção
class ExceptionHandler(Protocol):
    def __call__(
        self, request: Request, exc: Exception
    ) -> Coroutine[Any, Any, JSONResponse]:
        ...


# Exceção customizada
class ApiError(HTTPException):
    def __init__(
        self,
        status_code: int,
        msg: str,
        loc: list[Union[str, int]] | None = ["global"],
        type: Union[str, None] = None,
        exception: Exception | Any = None,
        debug: Union[str, None] = None,
    ):
        # Determina o tipo de erro padrão baseado no status code
        final_type = type or self._get_default_type(status_code)

        # Cria o detalhe do erro para a resposta
        error_detail = Detail(
            msg=msg, loc=loc or ["global"], type=final_type, debug=debug
        )

        # Faz o logging da exceção
        self._log_exception(status_code, msg, exception)

        # Chama o construtor da classe pai
        super().__init__(
            status_code=status_code,
            detail=ErrorSchema(detail=[error_detail]).model_dump()["detail"],
        )

    def _get_default_type(self, status_code: int) -> str:
        # Mapeia códigos de status para tipos de erro (pode ser expandido)
        types = {
            400: "bad_request",
            401: "unauthorized",
            403: "forbidden",
            404: "not_found",
            500: "internal_server_error",
        }
        return types.get(status_code, "unknown_error")

    def _log_exception(
        self,
        status_code: int,
        msg: str,
        exception: Exception | Any = None,
    ):
        # Determina o nível de log baseado no status code
        if status_code >= 500:
            log_level = logging.ERROR
        else:
            log_level = logging.WARNING

        # Mensagem de log base
        log_msg = f"HTTP {status_code}: {msg}"

        # Adiciona informações da exceção original se existir
        if exception:
            log_msg += (
                f" | Original exception: {type(exception).__name__}: {str(exception)}"
            )

        # Registra o log
        logger.log(log_level, log_msg, exc_info=exception)


# Handlers de exceção
async def custom_http_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handler para ApiError"""
    if not isinstance(exc, ApiError):
        return await generic_exception_handler(request, exc)

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler para HTTPException genéricas"""
    if not isinstance(exc, HTTPException):
        return await generic_exception_handler(request, exc)

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler para erros genéricos"""
    error_detail = ErrorSchema(
        detail=[
            Detail(
                loc=["global"],
                msg="Erro interno no servidor",
                type="internal_server_error",
                debug=str(exc) if exc else None,
            )
        ]
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_detail.model_dump(),
    )


RESPONSE: ResponseModels = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorSchema,
        "description": "Erro na requisição",
    },
}


# Configuração dos handlers
def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApiError, custom_http_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
