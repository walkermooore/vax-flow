from fastapi import APIRouter

from app import models
from app.db.session import sessionDep

router = APIRouter(prefix="/developer", tags=["Dev"])


@router.get("/list-all-routes", status_code=200)
def list_all_routes():
    """lista todas a rotas do API"""
    from app.db import list_functionality_names

    return list_functionality_names()


@router.post("/pop-all-functionality", status_code=200)
def pop_all_functionality(session: sessionDep):
    """cria todas a funcionalidades no banco de dados pegando os sumarios criados nas rotas como sufixo"""
    from app.db import pop_functionality_names

    pop_functionality_names(session)
    return "ok"


@router.post("/pop-initial-data", status_code=200)
def pop_initial_data(session: sessionDep):
    """popula a base de dados com os dados iniciais"""
    from app.db import pop_db

    pop_db(session)
    return "ok"


@router.get("/", status_code=200)
def list_all_database_name():
    response = []
    for key, value in models.__dict__.items():
        if (
            str(type(value))
            == "<class 'sqlalchemy.orm.decl_api.DeclarativeAttributeIntercept'>"
        ):
            response.append(key)
    return response
