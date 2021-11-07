from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from functools import lru_cache
from server.configuration.environment import get_environment_cached, ProfileEnvironment


class ProfileDB:

    Base = declarative_base()

    @staticmethod
    @lru_cache
    def create_async_engine_cached():
        environment = get_environment_cached()
        return create_async_engine(
            ProfileEnvironment.get_db_conn_async(environment.PROFILE_DATABASE_URL),
            echo=environment.DEFAULT_DB_ECHO,
            pool_size=environment.DEFAULT_DB_POOL_SIZE,
            max_overflow=environment.DEFAULT_DB_MAX_OVERFLOW,
            pool_pre_ping=environment.DEFAULT_DB_POOL_PRE_PING
        )

    @staticmethod
    def build_async_session_maker():
        return sessionmaker(
            ProfileDB.create_async_engine_cached(),
            expire_on_commit=False,
            class_=AsyncSession
        )

