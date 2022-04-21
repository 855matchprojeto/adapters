class CustomMsgException(Exception):

    def __init__(
        self,
        error_id,
        message,
        detail
    ):
        self.error_id = error_id
        self.message = message
        self.detail = detail


class EventHandlerNotImplementedException(CustomMsgException):

    def __init__(
        self,
        error_id='EVENT_HANDLER_NOT_IMPLEMENTED',
        message='Não foi encontrado um handler para o evento',
        detail=''
    ) -> None:
        super().__init__(error_id, message, detail)


class RequestFailException(CustomMsgException):

    def __init__(
        self,
        error_id='REQUEST_FAIL',
        message='Ocorreu um erro ao processar uma requisição',
        detail=''
    ) -> None:
        super().__init__(error_id, message, detail)

