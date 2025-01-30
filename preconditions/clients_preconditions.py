"""Предусловия связанные с подготовкой клиентов."""

from allure import title
from pytest import fixture
from test_tools.clients.restful_booker import RestfulBookerClient


@fixture
@title('Подготовлен клиент сервиса Restful Booker')
def setup_get_restful_booker_client(setup_get_config) -> RestfulBookerClient:
    """Подготовка клиента для работы с сервисом RestfulBooker."""
    restful_booker_config = setup_get_config['restful-booker']
    login, pwd, url = restful_booker_config['login'], restful_booker_config['password'], restful_booker_config['url']
    return RestfulBookerClient(username=login, password=pwd, endpoint=url)
