import asyncio
import boto3
from server.configuration.environment import Environment, get_environment_cached
from server.message_handlers.sqs_usuario_perfil_message_handler import SQSUsuarioPerfilMessage, \
    SQSUsuarioPerfilMessageProcessor
from server.message_handlers import Message, MessageProcessor
from server.message_handlers.sqs_usuario_perfil_message_handler import SQSUsuarioPerfilMessage, SQSUsuarioPerfilMessageProcessor
from server.configuration.custom_logging import get_main_logger
from server.configuration import exceptions
from server.configuration.db import ProfileDB
from server.repository.perfil_repository import PerfilRepository
from typing import Type
from server.configuration.custom_logging import Logger, MICROSERVICE_LOGGER_KWARGS


MAIN_LOGGER = get_main_logger()
SLEEP_TIME = 1


def get_sqs_usuario_perfil_message_processor(session, environment) -> SQSUsuarioPerfilMessageProcessor:
    return SQSUsuarioPerfilMessageProcessor(
        PerfilRepository(
            db_session=session, environment=environment
        )
    )


def get_message_dict(environment: Environment):
    return {
        environment.USER_PERFIS_SQS_NAME: {
            "message_class": SQSUsuarioPerfilMessage,
            "message_processor_builder": get_sqs_usuario_perfil_message_processor,
            "session_maker": ProfileDB.build_async_session_maker()
        }
    }


def get_sqs_client(environment: Environment) -> boto3.resource:
    return boto3.resource(
        'sqs',
        aws_access_key_id=environment.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=environment.AWS_SECRET_KEY,
        region_name=environment.AWS_REGION_NAME
    )


def get_all_queues(sqs_client, environment: Environment):
    return [
        dict(
            name=environment.USER_PERFIS_SQS_NAME,
            queue=sqs_client.get_queue_by_name(QueueName=environment.USER_PERFIS_SQS_NAME)
        )
    ]


def configura_logger():
    Logger(**MICROSERVICE_LOGGER_KWARGS).get_logger()


async def message_loop(queue_dict_list, message_dict: dict, environment: Environment):
    while True:
        for queue_dict in queue_dict_list:
            queue_name = queue_dict['name']
            queue = queue_dict['queue']
            await handle_messages_from_queue(
                queue,
                queue_name,
                message_dict[queue_name]['message_class'],
                message_dict[queue_name]['message_processor_builder'],
                message_dict[queue_name]['session_maker'],
                environment
            )
        await asyncio.sleep(SLEEP_TIME)


async def handle_messages_from_queue(
    queue, queue_name, message_class: Type[Message],
    message_processor_builder,
    session_maker, environment
):
    for sqs_msg in queue.receive_messages():
        MAIN_LOGGER.info(f"Mensagem recebida da fila {queue_name}: {sqs_msg.body}")
        await handle_message_from_queue(
            sqs_msg,
            message_class(sqs_msg.body),
            message_processor_builder,
            session_maker,
            environment
        )


async def handle_message_from_queue(
    sqs_msg, msg_obj: Message, message_processor_builder,
    session_maker, environment
):
    try:
        async with session_maker() as session:
            async with session.begin():
                message_processor = message_processor_builder(session, environment)
                await message_processor.process_message(msg_obj)
                sqs_msg.delete()
    except exceptions.CustomMsgException as ex:
        MAIN_LOGGER.warning("Erro detectado pela aplicacao")
        MAIN_LOGGER.exception(ex)
    except Exception as ex:
        MAIN_LOGGER.error("Ocorreu um erro não identificado pela aplicacao")
        MAIN_LOGGER.exception(ex)


async def init_message_handling_routine():
    configura_logger()
    MAIN_LOGGER.info("Iniciando rotina de tratamento de mensagens das filas")
    # Capturando o client SQS
    environment = get_environment_cached()
    sqs_client = get_sqs_client(environment)
    # Capturando as filas a serem "escutadas"
    queue_dict_list = get_all_queues(sqs_client, environment)
    message_dict = get_message_dict(environment)
    await message_loop(queue_dict_list, message_dict, environment)

