"""Тесты на получение списка всех пользователей."""

from allure import step, title, description, story, feature, link, epic

from test_tools.asserters import base_asserters


@epic('gRPC Example Service')
@feature('Пользователи')
@story('Получение списка всех пользователей')
@link(url='https://github.com/ritchiesinger/grpc_example_service', name="gRPC Example Service")
class TestGetUsers:  # pylint: disable=too-few-public-methods
    """Сценарии на получение списка всех пользователей."""

    @title('Успешное получение списка всех пользователей')
    @description('Позитивный сценарий получения списка всех пользователей.')
    def test_get_users_success(self, setup_get_grpc_example_service_client, setup_create_user_1):
        _ = setup_create_user_1
        with step('Получение списка всех пользователей'):
            response = setup_get_grpc_example_service_client.get_users()
            base_asserters.assert_condition(
                condition=len(response) > 0,
                allure_step_name='Полученный список непустой',
                error_text='Полученный список пустой!'
            )
            for result_index, result in enumerate(response):
                base_asserters.assert_equal(
                    expect='OK',
                    actual=result['responseMeta']['errorCode'],
                    name=f'#{result_index + 1}. error_code'
                )
