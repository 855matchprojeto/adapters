from pydantic import BaseSettings
from functools import lru_cache
import pathlib


@lru_cache
def get_environment_cached():
    return Environment(
        _env_file=f"{str(pathlib.Path(__file__).parents[2])}/.env/ADAPTER-PERFIS.env",
        _env_file_encoding="utf-8"
    )


class Environment(BaseSettings):

    # Configurações gerais dos bancos de dados

    DEFAULT_DB_ECHO: bool = True
    DEFAULT_DB_POOL_SIZE: int = 80
    DEFAULT_DB_MAX_OVERFLOW: int = 10
    DEFAULT_DB_POOL_PRE_PING: bool = True

    # Configurações AWS

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_KEY: str
    AWS_REGION_NAME: str

    # Configurações de serviços

    MS_PERFIS_ENDPOINT: str
    MS_PERFIS_INSERT_PERFIL_PATH: str

    MS_NOTIFICACAO_ENDPOINT: str
    MS_NOTIFICACAO_INSERT_NOTIFICACAO_PATH: str

    MS_AUTHENTICATOR_ENDPOINT: str
    MS_AUTHENTICATOR_GET_USER_BY_GUID_PATH: str

    # QUEUE NAME(S)

    USER_PERFIS_SQS_NAME: str
    INTERESSE_USUARIO_PROJETO_SQS_NAME: str

    # CONFIGURACAO SLEEP TIME

    SLEEP_TIME: int = 2

    # TOKEN OWNER

    OWNER_USER_TOKEN: str

    class Config:
        env_file = '.env/ADAPTER-PERFIS.env'
        env_file_encoding = 'utf-8'

