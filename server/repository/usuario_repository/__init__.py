import aiohttp
from server.configuration.environment import Environment
from server.configuration.custom_logging import get_main_logger
from server.configuration.exceptions import RequestFailException


MAIN_LOGGER = get_main_logger()


class UsuarioRepository:

    @staticmethod
    def build_auth_headers(environment: Environment):
        return {
            'Authorization': f'Bearer {environment.OWNER_USER_TOKEN}'
        }

    def __init__(self, environment: Environment = None):
        self.environment = environment

        self.auth_headers = self.build_auth_headers(environment)

    async def get_usuario_by_guid(self, guid_usuario: str) -> dict:
        MAIN_LOGGER.info(f"Capturando usuário no ms_authenticator {guid_usuario}")

        async with aiohttp.request(
            'GET',
            (
                f'{self.environment.MS_AUTHENTICATOR_ENDPOINT}'
                f'{self.environment.MS_AUTHENTICATOR_GET_USER_BY_GUID_PATH}'
                f'{guid_usuario}'
            ),
            headers=self.auth_headers
        ) as response:
            response: aiohttp.ClientResponse

            if str(response.status)[0] != '2':
                raise RequestFailException('Ocorreu um erro ao capturar o usuario por GUID')

            return await response.json()

