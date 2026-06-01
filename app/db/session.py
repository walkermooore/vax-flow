from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import core

__all__ = ["SessionLocal", "engine", "get_db", "sessionDep"]

# Configurando o log para exibir as queries
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine(
    core.settings.get_db_url(),
    pool_size=20,  # Número máximo de conexões persistentes
    max_overflow=40,  # Conexões extras temporárias sob demanda
    pool_timeout=30,  # Tempo de espera máximo para obter uma conexão
    pool_recycle=1800,  # Tempo para reciclar conexões (30 minutos)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db() -> AsyncGenerator[Session, None]:
    session = SessionLocal()
    try:
        session = SessionLocal()
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()


sessionDep = Annotated[Session, Depends(get_db)]
