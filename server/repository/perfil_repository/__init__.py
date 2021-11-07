from server.configuration.db import AsyncSession
from sqlalchemy import select, update, insert, delete, literal_column
from typing import List, Optional
from server.configuration.environment import Environment
from sqlalchemy.orm import selectinload
from server.models.perfis_service.usuario_model import Usuario
from server.models.perfis_service.perfil_model import Perfil


class PerfilRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def insere_perfil(self, perfil_dict: dict) -> Perfil:
        stmt = (
            insert(Perfil).
            returning(literal_column('*')).
            values(**perfil_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return Perfil(**row_to_dict)

    async def insere_usuario(self, usuario_dict: dict) -> Perfil:
        stmt = (
            insert(Usuario).
            returning(literal_column('*')).
            values(**usuario_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return Usuario(**row_to_dict)

