# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api import routers
from app.core import setup_exception_handlers
from app.core.config import settings
from app.core.logger import configure_logger

# from app.core.middleware import setup_middlewares

configure_logger()

app = FastAPI(
    title=settings.PROJECT_NAME if settings.PROJECT_NAME else "FastGen",
    docs_url=None if not settings.DEBUG else "/docs",
    redoc_url=None if not settings.DEBUG else "/redoc",
    openapi_url=None if not settings.DEBUG else "/openapi.json",
)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode vir do settings também
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)  # se usar sessões
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME if settings.PROJECT_NAME else "FastGen",
        version="1.0.0",
        description="Descrição da API",
        routes=app.routes,
    )

    # ✅ Remove todas as respostas 422 da documentação
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.get("responses", {}).pop("422", None)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# ⚠️ Atribuir ao app
# Routers e Handlers
app.openapi = custom_openapi
app.include_router(routers)
setup_exception_handlers(app)
