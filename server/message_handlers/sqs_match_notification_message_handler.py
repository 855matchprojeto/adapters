from server.message_handlers import Message, MessageProcessor
from server.repository.notification_repository import NotificacaoRepository
from server.repository.usuario_repository import UsuarioRepository
import json
from copy import deepcopy
from server.configuration.environment import Environment
from typing import List


"""
    Classes para tratamento de mensagens de notificações
    quando há algum evento do tipo:

    
    Aqui serão definidas as regras de negócio quando ocorrem 
    eventos de criação/edição de usuários
"""


class SQSMatchNotificationMessage(Message):

    def __init__(self, msg: str):
        super().__init__(msg)

    def extract_msg(self, msg: str) -> dict:
        msg_dict = json.loads(msg)
        return json.loads(msg_dict['Message'])

    def get_msg_event_name(self, msg_dict: dict) -> str:
        return msg_dict['type']

    def get_msg_body(self, msg_dict: dict) -> dict:
        new_msg_dict = deepcopy(msg_dict)
        del new_msg_dict['type']
        return msg_dict


class SQSMatchNotificationMessageProcessor(MessageProcessor):

    def __init__(
        self, environment: Environment = None,
        notification_repo: NotificacaoRepository = None,
        usuario_repo: UsuarioRepository = None
    ):
        super().__init__()
        self.notification_repo = notification_repo if notification_repo else NotificacaoRepository(environment)
        self.usuario_repo = usuario_repo if usuario_repo else UsuarioRepository(environment)

    async def build_payloads_event_interesse_usuario_projeto(self, msg_body: dict) -> List[dict]:
        guid_usuario: str = msg_body['user']['guid_usuario']

        aspas = '"'

        user_dict = await self.usuario_repo.get_usuario_by_guid(guid_usuario)
        guids_owners = msg_body['owners']
        project_dict: dict = msg_body['project']

        conteudo = f"O usuário {aspas}{user_dict['username']}{aspas} manifestou interesse" \
                   f" em seu projeto {aspas}{project_dict['titulo']}{aspas}"

        payloads = []

        for guid_owner in guids_owners:
            # Definindo payload para a tabela de notificacao no serviço de notificacao
            payloads.append({
                'is_read': False,
                'tipo': 'INTERESSE_USUARIO_PROJETO',
                'json_details': {
                    'user': user_dict,
                    'project': project_dict
                },
                'conteudo': conteudo,
                'guid_usuario': guid_owner
            })

        return payloads

    async def build_payload_event_interesse_projeto_usuario(self, msg_body: dict) -> dict:
        aspas = '"'

        guid_usuario: str = msg_body['user']['guid_usuario']

        user_dict = await self.usuario_repo.get_usuario_by_guid(guid_usuario)
        project_dict: dict = msg_body['project']

        conteudo = f"O projeto {aspas}{project_dict['titulo']}{aspas} se interessou em você!"

        payload = {
            'is_read': False,
            'tipo': 'INTERESSE_PROJETO_USUARIO',
            'json_details': {
                'user': user_dict,
                'project': project_dict
            },
            'conteudo': conteudo,
            'guid_usuario': guid_usuario
        }

        return payload

    async def build_payloads_event_match(self, msg_body: dict) -> List[dict]:
        guid_usuario: str = msg_body['user']['guid_usuario']

        user_dict = await self.usuario_repo.get_usuario_by_guid(guid_usuario)
        project_dict: dict = msg_body['project']
        guids_owners = msg_body['owners']

        payloads = []

        payloads.extend(self.build_payloads_event_match_projeto(user_dict, project_dict, guids_owners))
        payloads.append(self.build_payload_event_match_usuario(user_dict, project_dict))

        return payloads

    @staticmethod
    def build_payloads_event_match_projeto(
        user_dict: dict, project_dict: dict, guids_owners: List[str]
    ) -> List[dict]:
        aspas = '"'

        conteudo = f"Parabéns! Seu projeto {aspas}{project_dict['titulo']}{aspas}" \
                   f" deu match com o usuário {aspas}{user_dict['username']}{aspas}"

        payloads = []

        for guid_owner in guids_owners:
            payloads.append({
                'is_read': False,
                'tipo': 'MATCH_PROJETO',
                'json_details': {
                    'user': user_dict,
                    'project': project_dict
                },
                'conteudo': conteudo,
                'guid_usuario': guid_owner
            })

        return payloads

    @staticmethod
    def build_payload_event_match_usuario(
        user_dict: dict, project_dict: dict
    ) -> dict:
        aspas = '"'

        guid_usuario: str = user_dict['guid']

        conteudo = f"Parabéns! Você e o projeto {aspas}{project_dict['titulo']}{aspas} deram match!"

        payload = {
            'is_read': False,
            'tipo': 'MATCH_USUARIO',
            'json_details': {
                'user': user_dict,
                'project': project_dict
            },
            'conteudo': conteudo,
            'guid_usuario': guid_usuario
        }

        return payload

    async def handle_event_match(self, msg_body: dict, event_name: str):

        """
            Trata os eventos de MATCH entre usuário e projeto
        """

        payloads = await self.build_payloads_event_match(msg_body)

        for payload in payloads:
            await self.notification_repo.insere_notificacao(payload)

    async def handle_event_interesse_projeto_usuario(self, msg_body: dict, event_name: str):

        """
            Trata os eventos de interesse de um projeto em um usuário
        """

        payload = await self.build_payload_event_interesse_projeto_usuario(msg_body)

        await self.notification_repo.insere_notificacao(payload)

    async def handle_event_interesse_usuario_projeto(self, msg_body: dict, event_name: str):

        """
            Trata os eventos de interesse de um usuário em um projeto
        """

        payloads = await self.build_payloads_event_interesse_usuario_projeto(msg_body)

        for payload in payloads:
            await self.notification_repo.insere_notificacao(payload)

