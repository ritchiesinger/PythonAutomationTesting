"""Разные ожидалки сервиса Resful-Booker."""

from time import sleep

from allure import step

from test_tools.clients.restful_booker import RestfulBookerClient
from test_tools.asserters.base_asserters import assert_status_code


def wait_for_booking_deletion(client: RestfulBookerClient, booking_id: int, attempts: int = 10, interval: int = 2):
    """Ожидание удаления бронирования. Запрашиваем бронирование по ID до получения 404. Иначе - падаем.

    :param client: Клиент сервиса Restful-Booker.
    :param booking_id: Идентификатор бронирования удаление которого ожидаем.
    :param attempts: Кол-во попыток получить ожидаемый код ответа.
    :param interval: Интервал между попытками в секундах.
    """
    with step(f'Ожидание удаления бронирования {booking_id}. Попыток: {attempts}. Интервал: {interval}'):
        for attempt in range(attempts):
            with step(f'Попытка #{attempt + 1}. Получение данных бронирования'):
                get_response = client.get_booking(booking_id=booking_id)
                if get_response.status_code == 404:
                    break
            sleep(interval)
        assert_status_code(expect=404, response=get_response)
