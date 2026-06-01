import secrets

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

__all__ = ["settings"]


# Get the project root dynamically (one level above /app)
ROOT_DIR = Path(__file__).resolve().parent.parent  # /app
ENV_PATH = ROOT_DIR.parent / ".env"  # root/.env


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_ignore_empty=True,
        extra="ignore",
    )

    TOKEN_TYPE: str | None = Field(
        "Bearer", description="Prefixo da URL da API")
    SECRET_KEY: str | None = Field(
        description="Chave secreta para criptografia",
    )
    RESET_PASSWORD_TOKEN_EXPIRATION_MINUTES: int | None = Field(
        20, description="Validade do token de redefinição de senha em minutos"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = Field(
        86400, description="Validade do token de acesso em minutos"
    )

    PROJECT_NAME: str | None = Field(None, description="Nome do projeto")

    SMTP_TLS: bool | None = Field(None, description="Utilizar TLS para SMTP")
    SMTP_PORT: int | None = Field(None, description="Porta para conexão SMTP")
    SMTP_HOST: str | None = Field(None, description="Host para conexão SMTP")
    SMTP_PASSWORD: str | None = Field(
        None, description="Senha para conexão SMTP")
    EMAILS_FROM_EMAIL: str | None = Field(
        None, description="E-mail do remetente")
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int | None = Field(
        48, description="Validade do token de redefinição de e-mail em horas"
    )

    DEBUG: bool = Field(description="Modo de depuração")

    FIRST_SUPERUSER_EMAIL: str | None = Field(
        None, description="Email do superusuário")
    FIRST_SUPERUSER: str | None = Field(
        None, description="Nome de usuário do primeiro superusuário"
    )
    FIRST_SUPERUSER_PASSWORD: str | None = Field(
        None, description="Senha do primeiro superusuário"
    )

    TEMPLATES_DIR: str | None = Field(
        None, description="Diretório de templates")

    UPLOAD_DIR: str | None = Field(None, description="Diretório de upload")

    DATABASE_URL: str | None = Field(
        None, description="URL de conexão com o banco de dados (ex: sqlite:///./sql_app.db ou postgresql://...)"
    )

    def get_db_url(self):
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return "sqlite:///./sql_app.db"

    def get_async_db_url(self):
        if self.DATABASE_URL:
            # Converte para async se for postgresql
            if self.DATABASE_URL.startswith("postgresql://"):
                return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
            return self.DATABASE_URL
        return "sqlite+aiosqlite:///./sql_app.db"


settings = Settings()
