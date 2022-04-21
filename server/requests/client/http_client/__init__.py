import aiohttp
from server.requests.client import RequestClient


class HttpRequestClient(RequestClient):

    @staticmethod
    async def request(*args, **kwargs):
        return aiohttp.request(*args, **kwargs)

