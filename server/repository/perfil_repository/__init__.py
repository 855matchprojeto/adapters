import aiohttp.web_response
from server.requests.client.http_client import HttpRequestClient
from server.configuration.environment import Environment
from server.configuration.custom_logging import get_main_logger
from server.configuration.exceptions import RequestFailException


MAIN_LOGGER = get_main_logger()


class PerfilRepository:

    @staticmethod
    def build_auth_headers(environment: Environment):
        return {
            'Authorization': f'Bearer {environment.OWNER_USER_TOKEN}'
        }

    def __init__(self, request_client: HttpRequestClient, environment: Environment):
        self.environment = environment
        self.request_client = request_client if request_client else HttpRequestClient()

        self.auth_headers = self.build_auth_headers(environment)

    async def insere_perfil(self, perfil_dict: dict) -> dict:
        MAIN_LOGGER.info(f"Inserindo perfil no ms_perfil {perfil_dict}")

        response: aiohttp.web_response.json_response = await self.request_client.request(
            'POST', f'{self.environment.MS_PERFIS_ENDPOINT}/{self.environment.MS_PERFIS_INSERT_PERFIL_PATH}',
            json=perfil_dict,
            headers=self.auth_headers
        )

        if str(response.status)[0] != '2':
            raise RequestFailException('Ocorreu um erro ao inserir uma notificação')

        return response.json()

    async def insere_usuario(self, usuario_dict: dict) -> dict:
        MAIN_LOGGER.info(f"Inserindo usuário no ms_perfil {usuario_dict}")

        response: aiohttp.web_response.json_response = await self.request_client.request(
            'POST', f'{self.environment.MS_PERFIS_ENDPOINT}/{self.environment.MS_PERFIS_INSERT_USUARIO_PATH}',
            json=usuario_dict,
            headers=self.auth_headers
        )

        if str(response.status)[0] != '2':
            raise RequestFailException('Ocorreu um erro ao inserir uma notificação')

        return response.json()

