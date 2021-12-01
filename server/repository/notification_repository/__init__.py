from server.configuration.db import AsyncSession
from sqlalchemy import select, update, insert, delete, literal_column
from typing import List, Optional
from server.configuration.environment import Environment
from sqlalchemy.orm import selectinload
from server.models.notification_service.notificacao_model import Notificacao


class NotificacaoRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def insere_notificacao(self, notificacao_dict: dict) -> Notificacao:
        stmt = (
            insert(Notificacao).
            returning(literal_column('*')).
            values(**notificacao_dict)
        )
        query = await self.db_session.execute(stmt)
        row_to_dict = dict(query.fetchone())
        return Notificacao(**row_to_dict)

