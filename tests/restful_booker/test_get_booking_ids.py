"""Тесты на получение списка идентификаторов бронирований."""

from datetime import datetime

from allure import step, title, description, story, feature, link, epic
from pytest import mark

from test_tools.asserters import base_asserters
from test_tools.constants.restful_booker import RestulBookerConstants


@epic('Restful-Booker')
@feature('Бронирования')
@story('Получение списка существующих бронирований')
@link(url=f'{RestulBookerConstants.api_docs}#api-Booking-GetBookings', name="Restful-Booker API (GetBookingIds)")
class TestGetBookingIds:
    """Сценарии на получение списка идентификаторов бронирования."""

    @title('Успешное получение списка существующих бронирований (запрос без параметров)')
    @description('Позитивный сценарий получения списка существующих бронирований при запросе без параметров.')
    def test_get_booking_ids_success_200(self, setup_get_restful_booker_client):
        with step('Получение списка ID существующих бронирований (запрос без параметров)'):
            response = setup_get_restful_booker_client.get_booking_ids()
            base_asserters.assert_status_code(expect=200, response=response)
            base_asserters.assert_condition(
                condition=len(response.json()) > 0,
                allure_step_name='Полученный список непустой',
                error_text='Полученный список пустой'
            )

    @title('Успешное получение списка существующих бронирований с фильтром firstname')
    @description(
        'Позитивный сценарий получения списка существующих бронирований с фильром firstname.\n\n'
        'Для полноценной качественной проверки нужен доступ к БД, в которой мы бы запросили бронирования с аналогичной '
        'фильтрацией, и в тесте добавили бы проверку длины полученных списков: из БД и черезе API.'
    )
    @mark.parametrize("setup_create_booking", [{
        'firstname': 'Dima',
        'lastname': 'Kruzh',
        'totalprice': 111,
        'depositpaid': True,
        'checkin': '2018-01-01',
        'checkout': '2019-01-01',
        'additionalneeds': 'None'
    }], indirect=True)
    def test_get_booking_ids_firstname_filter_success_200(self, setup_get_restful_booker_client, setup_create_booking):
        client = setup_get_restful_booker_client
        filter_value = setup_create_booking['booking']['firstname']
        with step('Получение списка ID существующих бронирований с фильтрацией по имени'):
            get_list_response = client.get_booking_ids(firstname=filter_value)
            base_asserters.assert_status_code(expect=200, response=get_list_response)
            base_asserters.assert_condition(
                condition=len(get_list_response.json()) > 0,
                allure_step_name='Полученный список непустой',
                error_text='Полученный список пустой'
            )
        with step('Проверка имён (firstname) у полученных результатов'):
            for booking in get_list_response.json():
                with step(f'{booking["bookingid"]}'):
                    get_response = client.get_booking(booking_id=booking['bookingid'])
                    base_asserters.assert_status_code(expect=200, response=get_response)
                    booking_firstname, booking_id = get_response.json()['firstname'], booking['bookingid']
                    base_asserters.assert_condition(
                        condition=booking_firstname == filter_value,
                        allure_step_name=f'firstname. Ожидание: {filter_value}. Факт: {booking_firstname}',
                        error_text=f'Имя в бронировании {booking_id} не соответствует ожиданию!'
                    )

    @title('Успешное получение списка существующих бронирований с фильтром lastname')
    @description(
        'Позитивный сценарий получения списка существующих бронирований с фильром lastname.\n\n'
        'Для полноценной качественной проверки нужен доступ к БД, в которой мы бы запросили бронирования с аналогичной '
        'фильтрацией, и в тесте добавили бы проверку длины полученных списков: из БД и черезе API.'
    )
    def test_get_booking_ids_lastname_filter_success_200(self, setup_get_restful_booker_client, setup_create_booking):
        client = setup_get_restful_booker_client
        filter_value = setup_create_booking['booking']['lastname']
        with step('Получение списка ID существующих бронирований с фильтрацией по фамилии'):
            get_list_response = client.get_booking_ids(lastname=filter_value)
            base_asserters.assert_status_code(expect=200, response=get_list_response)
            base_asserters.assert_condition(
                condition=len(get_list_response.json()) > 0,
                allure_step_name='Полученный список непустой',
                error_text='Полученный список пустой'
            )
        with step('Проверка фамилий (lastname) у полученных результатов'):
            for booking in get_list_response.json():
                with step(f'ID = {booking["bookingid"]}'):
                    get_response = client.get_booking(booking_id=booking['bookingid'])
                    base_asserters.assert_status_code(expect=200, response=get_response)
                    booking_lastname, booking_id = get_response.json()['lastname'], booking['bookingid']
                    base_asserters.assert_condition(
                        condition=booking_lastname == filter_value,
                        allure_step_name=f'lastname. Ожидание: {filter_value}. Факт: {booking_lastname}',
                        error_text=f'Имя в бронировании {booking_id} не соответствует ожиданию!'
                    )

    @title('Успешное получение списка существующих бронирований с фильтром checkin')
    @description(
        'Позитивный сценарий получения списка существующих бронирований с фильром checkin.\n\n'
        'Для полноценной качественной проверки нужен доступ к БД, в которой мы бы запросили бронирования с аналогичной '
        'фильтрацией, и в тесте добавили бы проверку длины полученных списков: из БД и черезе API.'
    )
    def test_get_booking_ids_checkin_filter_success_200(self, setup_get_restful_booker_client, setup_create_booking):
        client = setup_get_restful_booker_client
        filter_value = setup_create_booking['booking']['bookingdates']['checkin']
        with step('Получение списка ID существующих бронирований с фильтрацией по времени заезда'):
            get_list_response = client.get_booking_ids(checkin=filter_value)
            base_asserters.assert_status_code(expect=200, response=get_list_response)
            base_asserters.assert_condition(
                condition=len(get_list_response.json()) > 0,
                allure_step_name='Полученный список непустой',
                error_text='Полученный список пустой'
            )
        with step('Проверка времени заезда (checkin) у полученных результатов'):
            for booking in get_list_response.json():
                with step(f'ID = {booking["bookingid"]}'):
                    get_response = client.get_booking(booking_id=booking['bookingid'])
                    base_asserters.assert_status_code(expect=200, response=get_response)
                    booking_checkin = get_response.json()['bookingdates']['checkin']
                    filter_value_date = datetime.strptime(filter_value, '%Y-%m-%d')
                    booking_date = datetime.strptime(booking_checkin, '%Y-%m-%d')
                    base_asserters.assert_condition(
                        condition=filter_value_date <= booking_date,
                        allure_step_name=f'Дата заезда {booking_checkin} позднее или равна {filter_value}',
                        error_text=f'Дата заезда {booking_checkin} ранее заданной в фильтре ({filter_value})!'
                    )

    @title('Успешное получение списка существующих бронирований с фильтром checkout')
    @description(
        'Позитивный сценарий получения списка существующих бронирований с фильром checkout.\n\n'
        'Для полноценной качественной проверки нужен доступ к БД, в которой мы бы запросили бронирования с аналогичной '
        'фильтрацией, и в тесте добавили бы проверку длины полученных списков: из БД и черезе API.'
    )
    def test_get_booking_ids_checkout_filter_success_200(self, setup_get_restful_booker_client, setup_create_booking):
        client = setup_get_restful_booker_client
        filter_value = setup_create_booking['booking']['bookingdates']['checkout']
        with step('Получение списка ID существующих бронирований с фильтрацией по дате выезда'):
            get_list_response = client.get_booking_ids(checkout=filter_value)
            base_asserters.assert_status_code(expect=200, response=get_list_response)
            base_asserters.assert_condition(
                condition=len(get_list_response.json()) > 0,
                allure_step_name='Полученный список непустой',
                error_text='Полученный список пустой'
            )
        with step('Проверка даты выезда (checkout) у полученных результатов'):
            for booking in get_list_response.json():
                with step(f'ID = {booking["bookingid"]}'):
                    get_response = client.get_booking(booking_id=booking['bookingid'])
                    base_asserters.assert_status_code(expect=200, response=get_response)
                    booking_checkout = get_response.json()['bookingdates']['checkout']
                    filter_value_date = datetime.strptime(filter_value, '%Y-%m-%d')
                    booking_date = datetime.strptime(booking_checkout, '%Y-%m-%d')
                    base_asserters.assert_condition(
                        condition=filter_value_date >= booking_date,
                        allure_step_name=f'Дата выезда {booking_checkout} раньше {filter_value}',
                        error_text=f'Дата выезда {booking_checkout} позднее или равна ({filter_value})!'
                    )

    @title('Получение ошибки при передаче невалидной даты в параметре checkin')
    @description(
        'Негативный сценарий получения списка существующих '
        'бронирований при запросе с невалидным параметром checkin.\n'
        'Ожидаем код 400 (BAD REQUEST).'
    )
    def test_get_booking_ids_with_invalid_checkin_failed_400(self, setup_get_restful_booker_client):
        with step('Получение списка ID существующих бронирований с передачей невалидного checkin'):
            response = setup_get_restful_booker_client.get_booking_ids(checkin='some_invalid_date_value')
            base_asserters.assert_status_code(expect=400, response=response)

    @title('Получение ошибки при передаче невалидной даты в параметре checkout')
    @description(
        'Негативный сценарий получения списка существующих '
        'бронирований при запросе с невалидным параметром checkin.\n'
        'Ожидаем код 400 (BAD REQUEST).'
    )
    def test_get_booking_ids_with_invalid_checkout_failed_400(self, setup_get_restful_booker_client):
        with step('Получение списка идентификаторов существующих бронирований'):
            response = setup_get_restful_booker_client.get_booking_ids(checkout='some_invalid_date_value')
            base_asserters.assert_status_code(expect=400, response=response)

    @title('Получение ошибки при значении checkout раньше checkin')
    @description(
        'Негативный сценарий получения списка существующих '
        'бронирований при запросе с отправкой checkout значением меньше чем checkin.\n'
        'Ожидаем код 400 (BAD REQUEST).'
    )
    def test_get_booking_ids_with_checkout_early_failed_400(self, setup_get_restful_booker_client):
        with step('Попытка получения списка идентификаторов существующих бронирований'):
            response = setup_get_restful_booker_client.get_booking_ids(checkout='2019-01-01', checkin='2020-01-01')
            base_asserters.assert_status_code(expect=400, response=response)
