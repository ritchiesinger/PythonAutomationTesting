"""Тесты авторизации."""

from allure import step, title, description, story, feature, link

from test_tools.asserters import base_asserters
from test_tools.constants.common import RestulBookerConstants


@feature('Авторизация')
@story('Получение авторизационного токена')
@link(url=f'{RestulBookerConstants.api_docs}#api-Auth-CreateToken', name="Restful-Booker API (CreateToken)")
class TestCreateToken:
    """Сценарии на получение авторизационного токена."""

    @title('Успешное получение авторизационного токена')
    @description('Позитивный сценарий получения авторизационного токена.')
    def test_post_auth_success_200(self, setup_get_restful_booker_client, setup_create_booking_1):
        with step('Получение авторизационного токена'):
            response = setup_get_restful_booker_client.auth(username='admin', password='password123')
            base_asserters.assert_status_code(expect=200, response=response)
            base_asserters.assert_condition(
                condition=response.json().get('token') is not None,
                allure_step_name='Токен успешно получен',
                error_text='Токен отсутстсует в ответе!'
            )
        with step('Удаление бронирования с полученным токеном'):
            response = setup_get_restful_booker_client.delete_booking(
                booking_id=setup_create_booking_1['bookingid'],
                auth_type='token'
            )
            base_asserters.assert_status_code(expect=201, response=response)
