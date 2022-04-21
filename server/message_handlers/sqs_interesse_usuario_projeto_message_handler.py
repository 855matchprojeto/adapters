from server.message_handlers import Message, MessageProcessor
from server.repository.notification_repository import NotificacaoRepository
import json
from copy import deepcopy


"""
    Classes para tratamento de mensagens do serviço de usuários.
    
    Aqui serão definidas as regras de negócio quando ocorrem 
    eventos de criação/edição de usuários
"""


class SQSInteresseUsuarioProjeto(Message):

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


class SQSInteresseUsuarioProjetoMessageProcessor(MessageProcessor):

    @staticmethod
    def get_payloads_event_create(msg_body: dict):

        user_dict: dict = msg_body['user']
        guids_owners = msg_body['owners']
        project_dict: dict = msg_body['project']

        conteudo = f"""O usuário "{user_dict['username']}" manifestou interesse no projeto "{project_dict['titulo']}"
        """

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

    def __init__(
        self,
        notification_repo: NotificacaoRepository
    ):
        super().__init__()
        self.notification_repo = notification_repo

    async def handle_event_create(self, msg_body: dict, event_name: str):

        """
            Trata os eventos de criação de usuário
        """

        payloads_dict = self.get_payloads_event_create(msg_body)

        for payload_dict in payloads_dict:
            await self.notification_repo.insere_notificacao(payload_dict)

