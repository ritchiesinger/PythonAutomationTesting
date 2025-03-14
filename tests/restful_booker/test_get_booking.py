"""Тесты на получение данных конкретного бронирования."""

from allure import step, title, description, story, feature, link, epic

from test_tools.asserters import base_asserters
from test_tools.constants.restful_booker import RestulBookerConstants
from test_tools.asserters.soft_asserter import SoftAssert


@epic('Restful-Booker')
@feature('Бронирования')
@story('Получение данных о бронировании')
@link(url=f'{RestulBookerConstants.api_docs}#api-Booking-GetBooking', name="Restful-Booker API (GetBooking)")
class TestGetBooking:
    """Сценарии на получение данных конкретного бронирования."""

    @title('Успешное получение данных бронирования по ID')
    @description('Позитивный сценарий получения данных бронирования по его идентификатору.')
    def test_get_booking_by_id_success_200(self, setup_get_restful_booker_client, setup_create_booking):
        with step('Получение данных о бронировании'):
            response = setup_get_restful_booker_client.get_booking(booking_id=setup_create_booking['bookingid'])
            SoftAssert(
                base_asserters.assert_status_code(expect=200, response=response, soft_assert=True),
                base_asserters.assert_equal(
                    expect=setup_create_booking['booking'],
                    actual=response.json(),
                    allure_step_name='Данные бронирования соответствуют ожиданию',
                    soft_assert=True
                )
            )

    @title('Получение ошибки при попытке запросить данные по несуществующему бронированию')
    @description('Негативный сценарий. Запрашиваем данные по заведомо несуществующему бронированию.')
    def test_get_booking_by_id_not_exist_failed_404(self, setup_get_restful_booker_client):
        with step('Получение данных о бронировании'):
            response = setup_get_restful_booker_client.get_booking(booking_id='9999999999')
            base_asserters.assert_status_code(expect=404, response=response)
