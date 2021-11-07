import logging
import sys


class Logger:

    @staticmethod
    def get_logger_by_name(logger_name: str):
        return logging.getLogger(logger_name)

    def __init__(self, logger_name: str, formatter: logging.Formatter):
        self.logger_name = logger_name
        self.formatter = formatter
        self.logger = logging.getLogger(logger_name)
        self.build_stdout_logger()
        self.logger.setLevel(logging.DEBUG)

    def build_stdout_logger(self):
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(self.formatter)
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

    def get_logger(self):
        return logging.getLogger(self.logger_name)


MICROSERVICE_LOGGER_NAME = "AUTHENTICATOR_LOGGER"
MICROSERVICE_LOGGER_KWARGS = {
    "logger_name": MICROSERVICE_LOGGER_NAME,
    "formatter": logging.Formatter(
        "{\n"
        f'\t"levelname": "%(levelname)s",\n'
        f'\t"asctime": "%(asctime)s",\n'
        f'\t"funcName": "%(funcName)s",\n'
        f'\t"module": "%(module)s",\n'
        f'\t"message": "%(message)s",\n'
        '}'
    )
}


def get_main_logger():
    return Logger.get_logger_by_name(MICROSERVICE_LOGGER_NAME)

