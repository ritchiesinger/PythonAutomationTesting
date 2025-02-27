"""Предусловия связанные с бронированиями в сервисе Restful-Booker."""

from typing import Any, Dict, List

from allure import title, step
from pytest import fixture

from test_tools.objects.booking import Booking
from test_tools.asserters import base_asserters
from test_tools.waiters.booking_waiters import wait_for_booking_deletion

# pylint: disable=redefined-outer-name  # Не нравятся линтеру зависимые фикстуры.


@fixture
@title('Подготовлен список для удаления бронирований после теста')
def setup_booking_ceanup_list(setup_get_restful_booker_client) -> List[int]:
    """Список, для ID бронирований. Все бронирования по этим ID после теста будут удалены."""
    cleanup_list = []
    yield cleanup_list
    client = setup_get_restful_booker_client
    with step('Удаление созданных в тесте бронирований'):
        for booking_id in cleanup_list:
            with step(f'{booking_id}'):
                with step('Удаление бронирования'):
                    delete_response = client.delete_booking(booking_id=booking_id)
                    base_asserters.assert_condition(
                        condition=delete_response.status_code in [201, 405],
                        allure_step_name='status_code имеет одно из значений: [201, 405]',
                        error_text=f'Неожиданный status_code ({delete_response.status_code})!'
                    )
                wait_for_booking_deletion(client=client, booking_id=booking_id)


@fixture
@title('Создано бронирование')
def setup_create_booking(request, setup_get_restful_booker_client, setup_booking_ceanup_list) -> Dict[str, Any]:
    """Создано тестовое бронирование.

    Фикстура может быть параметризована. Пример декоратора над тестом:
    @mark.parametrize("setup_create_booking", [{
        'firstname': 'Dima',
        'lastname': 'Kruzh',
        'totalprice': 111,
        'depositpaid': True,
        'checkin': '2018-01-01',
        'checkout': '2019-01-01',
        'additionalneeds': 'None'
    }], indirect=True)
    """
    client = setup_get_restful_booker_client
    if 'param' in dir(request):
        booking_obj_contract = request.param
    else:
        booking_obj_contract = {
            'firstname': 'Dima',
            'lastname': 'Kruzh',
            'totalprice': 111,
            'depositpaid': True,
            'checkin': '2018-01-01',
            'checkout': '2019-01-01',
            'additionalneeds': 'None'
        }
    booking_obj = Booking(**booking_obj_contract).to_json()
    create_response = client.create_booking(booking=booking_obj)
    base_asserters.assert_status_code(expect=200, response=create_response)
    setup_booking_ceanup_list.append(create_response.json()['bookingid'])
    return create_response.json()
