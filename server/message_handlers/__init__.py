import abc
from server.configuration import exceptions


class Message:

    def __init__(self, msg: str):
        extracted_msg = self.extract_msg(msg)
        self.body = self.get_msg_body(extracted_msg)
        self.event_name = self.get_msg_event_name(extracted_msg)

    @abc.abstractmethod
    def extract_msg(self, msg: str) -> dict:
        pass

    @abc.abstractmethod
    def get_msg_event_name(self, msg_dict: dict) -> str:
        """
            Retorna o evento da mensagem
        """
        pass

    @abc.abstractmethod
    def get_msg_body(self, msg_dict: dict) -> dict:
        """
            Retorna o conteúdo principal da mensagem
        """
        pass


class MessageProcessor:

    _handler_cache = None

    def __init__(self, *args):
        pass

    """
        Classe pai das classes que definem o processamento das mensagens
        Essas classes herdam a classe e obrigatoriamente definem métodos
        do tipo "event_handler_{event_name}" 
    """

    def process_message(self, msg: Message):

        if self._handler_cache is None:
            self._handler_cache = {}

        event_name = msg.event_name
        msg_body = msg.body
        event_handler = self._handler_cache.get(event_name, None)

        # Caso não esteja em cache
        if not event_handler:
            handler_name = f"handle_event_{event_name}"
            event_handler = getattr(self, handler_name, self.default_handler)
            self._handler_cache[handler_name] = event_handler

        return event_handler(msg_body, event_name)

    @staticmethod
    def default_handler(msg_body: dict, event_name: str):
        raise exceptions.EventHandlerNotImplementedException(
            detail=f"Não foi encontrado um handler para o evento {event_name}"
        )

