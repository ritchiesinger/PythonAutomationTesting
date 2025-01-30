"""Предусловия связанные с подготовкой клиентов."""

from allure import title
from pytest import fixture
from test_tools.clients.restful_booker import RestfulBookerClient


@fixture
@title('Подготовлен клиент сервиса Restful Booker')
def setup_get_restful_booker_client() -> RestfulBookerClient:
    """Подготовка клиента для работы с сервисом RestfulBooker."""
    return RestfulBookerClient(username='admin', password='password123')
