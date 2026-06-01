# app/core/router.py

from typing import Any, Callable, Optional, Type

from fastapi import APIRouter

from app.core.responses import RESPONSE, ApiSuccess


class CustomAPIRouter(APIRouter):
    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        response_model: Optional[Type[Any]] = None,
        responses: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        final_responses = RESPONSE.copy()
        if responses:
            final_responses.update(responses)

        if response_model is None:
            # Usa ApiSuccess vazio como padrão, se nenhum modelo foi passado
            response_model = ApiSuccess[Any]

        super().add_api_route(
            path,
            endpoint,
            response_model=response_model,
            responses=final_responses,
            **kwargs,
        )
