"""Предусловия связанные с подготовкой клиентов."""

from allure import title
from pytest import fixture
from test_tools.clients.restful_booker import RestfulBookerClient
from test_tools.clients.grpc_example_service import GrpcExampleServiceClient


@fixture
@title('Подготовлен клиент сервиса Restful Booker')
def setup_get_restful_booker_client(setup_get_config) -> RestfulBookerClient:
    """Подготовка клиента для работы с сервисом RestfulBooker."""
    restful_booker_config = setup_get_config['restful-booker']
    login, pwd, url = restful_booker_config['login'], restful_booker_config['password'], restful_booker_config['url']
    return RestfulBookerClient(username=login, password=pwd, endpoint=url)


@fixture
@title('Подготовлен клиент сервиса gRPC Example Service')
def setup_get_grpc_example_service_client(setup_get_config) -> GrpcExampleServiceClient:
    """Подготовка клиента для работы с gRPC Example Service."""
    restful_booker_config = setup_get_config['grpc-example-service']
    return GrpcExampleServiceClient(endpoint=restful_booker_config['url'])
