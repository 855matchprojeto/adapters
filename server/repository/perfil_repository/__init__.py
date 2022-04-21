import aiohttp
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

    def __init__(self, environment: Environment = None):
        self.environment = environment
        self.auth_headers = self.build_auth_headers(environment)

    async def insere_perfil(self, perfil_dict: dict) -> dict:
        MAIN_LOGGER.info(f"Inserindo perfil no ms_perfil {perfil_dict}")

        async with aiohttp.request(
            'POST', f'{self.environment.MS_PERFIS_ENDPOINT}{self.environment.MS_PERFIS_INSERT_PERFIL_PATH}',
            json=perfil_dict,
            headers=self.auth_headers
        ) as response:
            response: aiohttp.ClientResponse

            if str(response.status)[0] != '2':
                raise RequestFailException('Ocorreu um erro ao inserir uma notificação')

            return await response.json()

