import json

from fastapi import (APIRouter, BackgroundTasks, Depends, Header, Request,
                     Response)

from app.auth import decode_token, encode_token
from app.core import ApiError, get_password_hash, settings, verify_password
from app.db.session import sessionDep
from app.models import (Papeis, PapeisFuncionalidades, Usuarios,
                        UsuariosFuncionalidades)
from app.schema import (EsqueciSenha, Login, NovaSenha, ResponseEsqueciSenha,
                        ResponseEsqueciSenhaCodigo, ResponseLoginAcessToken,
                        ResponseLoginSessionToken)
from app.util import generate_code, normalize_uper, send_email, template_string

router = APIRouter(tags=["Auth"])


@router.post(
    "/login/access-token",
    operation_id="login_access_token",
    response_model=ResponseLoginAcessToken,
)
def login(session: sessionDep, login: Login = Depends(Login.as_form)):
    """Logar"""

    user = Usuarios.login(session, "nome_usuario", login.username, login.password)
    role_keys = [0]
    all_permissions = []
    papel = ""
    if user.papel_id:
        role_data = Papeis.query_params(
            session,
            all_data=True,
            filters={"id": user.papel_id},
        ).data
        if len(role_data) > 0:
            if role_data[0].ativo:
                papel = role_data[0].nome
                papeis_funcionalidades = PapeisFuncionalidades.query_params(
                    session,
                    all_data=True,
                    filters={"papel_id": user.papel_id},
                    expand=["funcionalidades"],
                    limit=1000,
                ).data
                for papeis_funcionalidades in papeis_funcionalidades:
                    all_permissions.append(
                        papeis_funcionalidades.funcionalidades.escopo
                    )
                    role_keys.append(papeis_funcionalidades.funcionalidades.chave)
            if len(role_keys) == 0:
                role_keys = [0]
    user_keys = [0]
    user_functionality_data = UsuariosFuncionalidades.query_params(
        session, all_data=True, filters={"usuario_id": user.id}
    ).data
    if len(user_functionality_data) > 0:
        for user_functionality in user_functionality_data:
            all_permissions.append(user_functionality.funcionalidades.escopo)
            user_keys.append(user_functionality.funcionalidades.key)

    if len(user_keys) == 0:
        user_keys = [0]

    all_keys = sorted(set(user_keys + role_keys))

    sub = {
        "usuario_id": str(user.id),
        "nome_completo": str(user.nome_completo) if user.nome_completo else "",
        "chave": all_keys,
    }

    token = encode_token(
        json.dumps(sub),
        settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    response = ResponseLoginAcessToken(
        access_token=token,
        token_type=settings.TOKEN_TYPE,
        permission=all_permissions,
        user=user,
        papel=papel,
    )
    return response


@router.post(
    "/login/session-token",
    operation_id="login_session_token",
    response_model=ResponseLoginSessionToken,
)
def login(
    request: Request,
    response: Response,
    session: sessionDep,
    login: Login = Depends(Login.as_form),
):
    """Logar com sessão"""

    user = Usuarios.login(session, "nome_usuario", login.username, login.password)
    all_keys = [
        papeis_funcionalidades.funcionalidades.chave
        for papeis_funcionalidades in PapeisFuncionalidades.query_params(
            session,
            all_data=True,
            filters={"papel_id": user.papel_id},
            expand=["funcionalidades"],
        ).data
    ]
    if len(all_keys) == 0:
        all_keys[0]
    sub = {
        "usuario_id": str(user.id),
        "chave": all_keys,
    }
    token = encode_token(
        json.dumps(sub),
        settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    try:
        request.session["token"]
    except Exception as e:
        raise ApiError(
            status_code=404,
            loc=["body"],
            msg="Login por sessão nao esta habilitado, consulte o desenvolvedor",
            type="session.auth",
            exception=e,
        )

    return ResponseLoginSessionToken(user=user)


# TODO: implementar backgroud task no envio de email e transformar rota em async
@router.post(
    "/esqueci-senha/",
    operation_id="esqueci_senha",
    response_model=ResponseEsqueciSenha,
)
async def esqueci_senha(
    session: sessionDep,
    email: EsqueciSenha,
    background_tasks: BackgroundTasks,
):
    """Esqueci minha senha"""

    user = Usuarios.get(session, "email", email.email)
    if not user:
        raise ApiError(
            status_code=400,
            loc=["body", "email"],
            msg=f"Email não encontrado",
            type="value_error.routes.login",
        )
    code = await generate_code()

    background_tasks.add_task(
        send_email,
        email.email,
        settings.PROJECT_NAME,
        template_string(
            "reset_password.html",
            {
                "code": code,
            },
        ),
    )

    hash_to_string = get_password_hash(code).decode("utf-8")

    sub = {"code": hash_to_string, "id": str(user.id)}
    response = ResponseEsqueciSenha(
        token=encode_token(
            json.dumps(sub),
            settings.RESET_PASSWORD_TOKEN_EXPIRATION_MINUTES,
        )
    )
    return response


@router.post(
    f"/esqueci-senha/code",
    operation_id="esqueci_senha_codigo",
    response_model=ResponseEsqueciSenhaCodigo,
)
async def redefinir_senha_codigo(
    code: str,
    Authentication: str = Header(...),
):
    """Compara o codigo enviado para o email"""

    code = normalize_uper(code)
    token_content = decode_token(Authentication)
    if not verify_password(code, token_content["code"]):
        raise ApiError(
            status_code=404,
            loc=["body", "code"],
            msg=f"Código inválido",
            type="value_error.routes.login",
        )
    sub = {"status": "approved", "id": token_content["id"]}
    response = ResponseEsqueciSenhaCodigo(
        token=encode_token(
            json.dumps(sub),
            settings.RESET_PASSWORD_TOKEN_EXPIRATION_MINUTES,
        )
    )
    return response


@router.put("/nova-senha/", operation_id="nova_senha")
def put_password(
    session: sessionDep,
    senha: NovaSenha,
    Authentication: str = Header(...),
):
    """Altera a senha do usuarios"""
    sub = decode_token(Authentication)
    Usuarios.update(
        session,
        sub["id"],
        **senha.model_dump(
            exclude_unset=True,
        ),
    )
    return "Senha alterada"
