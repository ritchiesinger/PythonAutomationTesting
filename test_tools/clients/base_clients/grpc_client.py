"""Клиент для работы с GRPC."""
from json import dumps
from typing import Any

from google.protobuf.json_format import MessageToDict
from grpc import insecure_channel

from test_tools.common import attach_json
from test_tools.common import get_logger
from test_tools.constants.common import GRPCMethodType

logger = get_logger('grpc_client')


def log_request(func):
    """Декоратор для логирования gRPC запросов/ответов и вложений в Allure."""
    def wrapper(*args, **kwargs):
        client = args[0]
        method_type, method_name, request = kwargs.get("method_type"), kwargs.get("method_name"), kwargs.get("request")
        verbose_url = f'{client.endpoint}/{method_name}'
        verbose_method_type = method_type.replace('_', ' ')
        invoke_log_str = f'Invoke {verbose_method_type} {verbose_url}'
        logger.debug(invoke_log_str)
        if method_type == GRPCMethodType.CLIENT_STREAM:
            for item_index, item in enumerate(request):
                logger.debug('REQUEST MESSAGE #%s: %s', item_index + 1, MessageToDict(item))
                attach_json(obj=MessageToDict(item), name=f'REQUEST MESSAGE #{item_index + 1} {verbose_url}')
        elif method_type in (GRPCMethodType.UNARY, GRPCMethodType.SERVER_STREAM):
            log_str_dict_msg = dumps(MessageToDict(request), ensure_ascii=False)
            logger.debug('REQUEST MESSAGE: %s', log_str_dict_msg)
            attach_json(obj=MessageToDict(request), name=f'REQUEST MESSAGE {verbose_url}')
        original_result = func(*args, **kwargs)
        if method_type in (GRPCMethodType.CLIENT_STREAM, GRPCMethodType.UNARY):
            logger.debug('RESPONSE MESSAGE: %s', original_result)
            attach_json(obj=original_result, name='RESPONSE MESSAGE')
        elif method_type == GRPCMethodType.SERVER_STREAM:
            for item_index, item in enumerate(original_result):
                logger.debug('RESPONSE MESSAGE #%s: %s', item_index + 1, item)
                attach_json(obj=item, name=f'RESPONSE MESSAGE #{item_index + 1}')
        elif method_type == GRPCMethodType.BIDIRECTIONAL:
            for item_index, item in enumerate(request):
                request_message = MessageToDict(item)
                attach_json(obj=request_message, name=f'REQUEST MESSAGE #{item_index + 1} {verbose_url}')
                attach_json(obj=original_result[item_index], name=f'RESPONSE MESSAGE #{item_index + 1}')
                logger.debug('REQUEST MESSAGE #%s: %s', item_index + 1, request_message)
                logger.debug('RESPONSE MESSAGE #%s: %s', item_index + 1, original_result[item_index])
        return original_result
    return wrapper


class GRPCClient:  # pylint: disable=too-few-public-methods
    """Клиент для работы с GRPC."""

    def __init__(self, endpoint: str, stub: type):
        """Клиент для работы с GRPC."""
        self.endpoint = endpoint
        self.stub = stub

    def __str__(self):
        return f'<gRPC Client. endpoint="{self.endpoint}">'

    def __repr__(self):
        return self.__str__()

    @log_request
    def send(self, method_type: GRPCMethodType | str, method_name: str, request) -> Any:
        """Отправка GRPC запроса.

        :param method_type: Тип GRPC запроса.
        :param method_name: Имя вызываемого метода.
        :param request: Данные которые отправляются в запросе.
        """
        with insecure_channel(self.endpoint) as channel:
            match method_type:
                case GRPCMethodType.SERVER_STREAM:
                    response = getattr(self.stub(channel=channel), method_name)(request)
                    return [MessageToDict(item, always_print_fields_with_no_presence=True) for item in list(response)]
                case GRPCMethodType.CLIENT_STREAM:
                    return MessageToDict(getattr(self.stub(channel=channel), method_name)(
                        iter(request)), always_print_fields_with_no_presence=True
                    )
                case GRPCMethodType.UNARY:
                    return MessageToDict(getattr(self.stub(channel=channel), method_name)(
                        request), always_print_fields_with_no_presence=True
                    )
                case GRPCMethodType.BIDIRECTIONAL:
                    response = getattr(self.stub(channel=channel), method_name)(iter(request))
                    return [MessageToDict(item, always_print_fields_with_no_presence=True) for item in list(response)]
                case _:
                    raise TypeError(f'Неизвестный тип запроса: "{method_type}"!')
