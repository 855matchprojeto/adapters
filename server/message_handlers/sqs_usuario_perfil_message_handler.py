from server.message_handlers import Message, MessageProcessor
from server.repository.perfil_repository import PerfilRepository
from server import utils
import json
from server.configuration.environment import Environment


"""
    Classes para tratamento de mensagens do serviço de usuários.
    
    Aqui serão definidas as regras de negócio quando ocorrem 
    eventos de criação/edição de usuários
"""


class SQSUsuarioPerfilMessage(Message):

    def __init__(self, msg: str):
        super().__init__(msg)

    def extract_msg(self, msg: str) -> dict:
        msg_dict = json.loads(msg)
        return json.loads(msg_dict['Message'])

    def get_msg_event_name(self, msg_dict: dict) -> str:
        return msg_dict['type']

    def get_msg_body(self, msg_dict: dict) -> dict:
        return msg_dict['user']


class SQSUsuarioPerfilMessageProcessor(MessageProcessor):

    @staticmethod
    def get_payloads_event_create(msg_body: dict):

        # Definindo payload para a tabela de usuario no serviço de perfis
        user_payload = msg_body
        user_payload['updated_at'] = user_payload['created_at']

        # Definindo payload para a tabela de perfis no serviço de perfis
        profile_payload = {
            'nome_exibicao': msg_body['nome'],
            'nome_exibicao_normalized': utils.normalize_string(msg_body['nome']),
            'guid_usuario': msg_body['guid']
        }

        return {
            'user': user_payload,
            'profile': profile_payload
        }

    def __init__(
        self, environment: Environment = None,
        profile_repo: PerfilRepository = None
    ):
        super().__init__()
        self.profile_repo = profile_repo if profile_repo else PerfilRepository(environment)

    async def handle_event_create(self, msg_body: dict, event_name: str):

        """
            Trata os eventos de criação de usuário
        """

        payload_dict = SQSUsuarioPerfilMessageProcessor.get_payloads_event_create(msg_body)
        await self.profile_repo.insere_perfil(payload_dict)

