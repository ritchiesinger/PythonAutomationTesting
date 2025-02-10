"""Клиент для работы с учебным GRPC сервисом."""

# pylint: disable=no-member # grpc_tools.protoc криво генерит файлы схемы. Так-то они работают.

from typing import Any, Dict, List

from schema.grpc_example_service import GrpcExampleService_pb2_grpc, GrpcExampleService_pb2
from test_tools.clients.base_clients.grpc_client import GRPCClient
from test_tools.common import get_logger
from test_tools.constants.common import GRPCMethodType

logger = get_logger('grpc_example_service_client')


class GrpcExampleServiceClient(GRPCClient):
    """Клиент для работы с учебным GRPC сервисом."""

    def __init__(self, endpoint):
        """Клиент для работы с учебным GRPC сервисом."""
        super().__init__(endpoint=endpoint, stub=GrpcExampleService_pb2_grpc.GrpcExampleServiceStub)

    def add_users(self, users: List[Dict[str, str]]) -> Dict[str, Any]:
        """Добавление одного или более пользователей.

        :param users: Список объектов пользователей.
        :return: Ответ сервиса.
        """
        logger.info('Добавление пользователей.')
        request = [GrpcExampleService_pb2.UserInfo(**item) for item in users]
        return self.send(method_type=GRPCMethodType.CLIENT_STREAM, method_name='AddUsers', request=request)

    def get_users(self) -> List[Dict[str, Dict[str, str]]]:
        """Получение списка всех пользователей.

        :return: Список из объектов с данными пользователей.
        """
        logger.info('Получение списка всех пользователей.')
        request = GrpcExampleService_pb2.Empty()
        return self.send(method_type=GRPCMethodType.SERVER_STREAM, method_name='GetUsers', request=request)

    def get_user_by_login(self, login: str) -> Dict[str, Dict[str, str]]:
        """Получение списка всех пользователей.

        :param login: Логин запрашиваемого пользователя.
        :return: Данные пользователя.
        """
        logger.info('Получение данных пользователя.')
        request = GrpcExampleService_pb2.GetUserByLoginRequest(login=login)
        return self.send(method_type=GRPCMethodType.UNARY, method_name='GetUserByLogin', request=request)

    def delete_users(self, users_ids: List[int]) -> List[Dict[str, Any]]:
        """Удаление одного или более пользователей по их ID.

        :param users_ids: Список идентификаторов пользователей на удаление.
        :return: Список объектов - результатов удаления каждого пользователя.
        """
        logger.info('Удаление пользователей.')
        request = [GrpcExampleService_pb2.DeleteUserInfo(id=item) for item in users_ids]
        return self.send(method_type=GRPCMethodType.BIDIRECTIONAL, method_name='DeleteUsers', request=request)


if __name__ == '__main__':
    client = GrpcExampleServiceClient(endpoint='localhost:50051')
    client.add_users(users=[{'login': 'qqdq113', 'email': 'rere', 'city': 'fffff'}])
    client.get_user_by_login(login='asdf11')
    client.get_users()
    client.delete_users(users_ids=[5, 4, 12])
