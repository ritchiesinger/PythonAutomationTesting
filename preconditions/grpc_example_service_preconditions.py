"""Предусловия связанные с бронированиями в сервисе Restful-Booker."""

from typing import Any, Dict, List
from uuid import uuid4

from allure import title, step
from pytest import fixture

from test_tools.asserters import base_asserters

# pylint: disable=redefined-outer-name  # Не нравятся линтеру зависимые фикстуры.


@fixture
@title('Подготовлен список для удаления пользователей после теста')
def setup_users_cleanup_list(setup_get_grpc_example_service_client) -> List[int]:
    """Список, для ID пользователей. Все бронирования по этим ID после теста будут удалены."""
    cleanup_list: List[int] = []
    yield cleanup_list
    client = setup_get_grpc_example_service_client
    with step('Удаление созданных в тесте пользователей'):
        response = client.delete_users(users_ids=cleanup_list)
        for result_index, result in enumerate(response):
            base_asserters.assert_equal(
                expect='OK',
                actual=result['responseMeta']['errorCode'],
                name=f'#{result_index + 1}. errorCode'
            )


@fixture
@title('Добавлен Пользователь 1')
def setup_create_user_1(setup_get_grpc_example_service_client, setup_users_cleanup_list) -> Dict[str, Any]:
    """Создано тестовое бронирование."""
    client = setup_get_grpc_example_service_client
    with step('Добавление пользователя'):
        user_obj = {'login': f'Richard_{uuid4()}', 'email': 'richard@some.com', 'city': 'City'}
        create_response = client.add_users(users=[user_obj])
        base_asserters.assert_equal(
            expect='OK',
            actual=create_response['addResults'][0]['responseMeta']['errorCode'],
            name='errorCode'
        )
        setup_users_cleanup_list.append(create_response['addResults'][0]['userInfo']['id'])
        return create_response
