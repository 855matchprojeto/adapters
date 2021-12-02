from sqlalchemy import Column, BigInteger, String
from server.models.perfis_service import PerfilBase
from server.models.perfis_service import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Perfil(Base, PerfilBase):

    def __init__(self, **kwargs):
        super(Perfil, self).__init__(**kwargs)

    __tablename__ = "tb_perfil"

    guid = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guid_usuario = Column(UUID(as_uuid=True), nullable=False, unique=True)
    bio = Column(String())

    nome_exibicao = Column(String())
    nome_exibicao_normalized = Column(String())

    url_imagem = Column(String())

