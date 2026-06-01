# app/utils/funcionalidade.py
import logging

from app import api, models, schema

logger = logging.getLogger(__name__)


def list_functionality_names():
    method_to_action = {
        "GET": "Consultar",
        "POST": "Criar",
        "PATCH": "Editar",
        "DELETE": "Excluir",
        "PUT": "Modificar",
    }

    return [
        {
            "path": route.path,
            "methods": list(route.methods)[0],
            "summary": getattr(route, "summary", None),
        }
        for route in api.routers.routes
        if hasattr(route, "methods") and hasattr(route, "path")
    ]

import re

def remover_parametro_final(path):
    """
    Remove o último parâmetro entre chaves, mantendo a estrutura do path
    """
    # Remove qualquer conteúdo entre { } no final do path
    path_limpo = re.sub(r'/\{[^}]*\}$', '', path)
    
    # Garante que termina com barra
    if path_limpo and not path_limpo.endswith('/'):
        path_limpo += '/'
    
    return path_limpo


def pop_functionality_names(session):
    method_to_scope = {
        "GET": "read",
        "POST": "create",
        "PATCH": "update",
        "DELETE": "delete",
        "PUT": "update",
    }

    for route in api.routers.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            method = list(route.methods)[0]
            caminho = remover_parametro_final(route.path)
            summary = getattr(route, "summary", None)
            categoria = route.tags[0] if route.tags else "default"
            escopo = f"{caminho.replace('/', '')}:{method_to_scope.get(method, method)}"

            if not summary:
                continue

            exists = (
                session.query(models.Funcionalidades)
                .filter_by(nome=summary, caminho=caminho, metodo=method)
                .first()
            )
            if exists:
                logger.info(f"Funcionalidade já existe: {summary} ({method} {caminho})")
                continue

            data = models.Funcionalidades(
                **schema.PostFuncionalidades(
                    nome=summary,
                    caminho=caminho,
                    metodo=method,
                    escopo=escopo,
                    categoria=categoria,
                ).model_dump()
            )

            data.create(session)
            logger.info(f"Funcionalidade criada: {summary} ({method} {caminho})")

    logger.info("Criação de funcionalidades concluída.")
