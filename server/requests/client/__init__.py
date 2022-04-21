import abc


class RequestClient:

    @staticmethod
    @abc.abstractmethod
    async def request(*args, **kwargs):
        pass

