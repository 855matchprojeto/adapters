import aiohttp.web_response
from server.requests.client.http_client import HttpRequestClient
from server.configuration.environment import Environment
from server.configuration.custom_logging import get_main_logger
from server.configuration.exceptions import RequestFailException


MAIN_LOGGER = get_main_logger()


class NotificacaoRepository:

    @staticmethod
    def build_auth_headers(environment: Environment):
        return {
            'Authorization': f'Bearer {environment.OWNER_USER_TOKEN}'
        }

    def __init__(self, request_client: HttpRequestClient, environment: Environment):
        self.environment = environment
        self.request_client = request_client if request_client else HttpRequestClient()

        self.auth_headers = self.build_auth_headers(environment)

    async def insere_notificacao(self, notificacao_dict: dict) -> dict:
        MAIN_LOGGER.info(f"Inserindo notificação {notificacao_dict}")

        response: aiohttp.web_response.json_response = await self.request_client.request(
            'POST',
            f'{self.environment.MS_NOTIFICACAO_ENDPOINT}/{self.environment.MS_NOTIFICCAO_INSERT_NOTIFICACAO_PATH}',
            json=notificacao_dict,
            headers=self.auth_headers
        )

        if str(response.status)[0] != '2':
            raise RequestFailException('Ocorreu um erro ao inserir uma notificação')

        return response.json()

