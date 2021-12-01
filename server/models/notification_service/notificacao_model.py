from sqlalchemy import Column, BigInteger, String, Boolean
from server.models.notification_service import NotificationBase
from server.configuration import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from server.models.notification_service import Base


class Notificacao(Base, NotificationBase):

    def __init__(self, **kwargs):
        super(Notificacao, self).__init__(**kwargs)

    __tablename__ = "tb_notificacao"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True)
    guid_usuario = Column(UUID(as_uuid=True), nullable=False, unique=False)

    conteudo = Column(String)
    is_read = Column(Boolean, default=False)

