import re
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

    # Configurações de banco de dados

    PROFILE_DATABASE_URL: str

    # QUEUE NAME(S)

    USER_PERFIS_SQS_NAME: str

    class Config:
        env_file = '.env/ADAPTER-PERFIS.env'
        env_file_encoding = 'utf-8'


class ProfileEnvironment(BaseSettings):

    @staticmethod
    def get_db_conn_async(database_url: str):
        return re.sub(r'\bpostgres://\b', "postgresql+asyncpg://", database_url, count=1)

    @staticmethod
    def get_db_conn_default(database_url: str):
        return re.sub(r'\bpostgres://\b', "postgresql://", database_url, count=1)

