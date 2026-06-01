from app import core, models, schema
from app.db.session import SessionLocal

__all__ = ["pop_db"]


role = [
    {
        "nome": "Admin",
        "descricao": """Responsabilidades: O Admin tem controle total sobre o sistema ou plataforma, o que significa que pode adicionar, modificar ou excluir qualquer conteúdo ou usuário. """,
    },
    {
        "nome": "Gestor",
        "descricao": """Responsabilidades: O Gestor tem controle sobre o sistema ou plataforma, o que significa que pode adicionar, modificar ou excluir qualquer conteúdo ou usuário. """,
    },
    {
        "nome": "Tecnico",
        "descricao": """Responsabilidades: O Tecnico tem controle sobre o sistema ou plataforma, o que significa que pode adicionar, modificar ou excluir qualquer conteúdo ou usuário. """,
    },
]


def pop_db(session) -> None:
    """Caso exista dados iniciais no banco da aplicação, escrever sua inserçao"""

    for data in role:
        if models.Papeis.get(session, "nome", data["nome"]):
            pass
        else:
            role_data = models.Papeis(**data)
            role_data.create(session)
    role_admin = models.Papeis.get(session, "nome", "Admin")

    if role_admin:
        all_functionality = models.Funcionalidades.query_params(
            session, all_data=True, limit=1000
        ).data
        for functionality in all_functionality:
            query_result = models.PapeisFuncionalidades.query_params(
                session,
                all_data=True,
                limit=1000,
                filters={
                    "papel_id": role_admin.id,
                    "funcionalidade_id": functionality.id,
                },
            )
            if len(query_result.data) > 0:
                pass
            else:
                role_functionality_data = models.PapeisFuncionalidades(
                    papel_id=role_admin.id,
                    funcionalidade_id=functionality.id,
                )
                role_functionality_data.create(session)
    if role_admin:
        if models.Usuarios.get(
            session,
            "nome_usuario",
            (
                core.settings.FIRST_SUPERUSER
                if core.settings.FIRST_SUPERUSER
                else "admin"
            ),
        ):
            pass
        else:
            usuario_schema = schema.PostUsuarios(
                nome_usuario=(
                    core.settings.FIRST_SUPERUSER
                    if core.settings.FIRST_SUPERUSER
                    else "admin"
                ),
                nome_completo="Administrador do Sistema",
                senha=(
                    core.settings.FIRST_SUPERUSER_PASSWORD
                    if core.settings.FIRST_SUPERUSER_PASSWORD
                    else "admin"
                ),
                cargo="Administrador",
                email=(
                    core.settings.FIRST_SUPERUSER_EMAIL
                    if core.settings.FIRST_SUPERUSER_EMAIL
                    else "juniormarans@gmail.com"
                ),
                ativo=True,
                papel_id=role_admin.id,
            )
            user_data = models.Usuarios(**usuario_schema.model_dump())
            user_data.create(session)

            
# Allow direct execution: uv run python -m app.db.init_db
if __name__ == "__main__":
    session = SessionLocal()
    try:
        pop_db(session)
        print("✅ Database populated successfully!")
    except Exception as e:
        print(f"❌ Error populating DB: {e}")
        session.rollback()
    finally:
        session.close()