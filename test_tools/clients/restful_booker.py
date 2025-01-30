"""HTTP клиент для работы с сервисом restful-booker. https://restful-booker.herokuapp.com/apidoc/index.html."""

from base64 import b64encode
from typing import Any, Dict

from requests import Response

from test_tools.clients.http_client import HTTPClient
from test_tools.constants.headers import Headers, ContentType, Accept
from test_tools.objects.booking import Booking


class RestfulBookerClient(HTTPClient):
    """HTTP клиент для работы с сервисом restful-booker. https://restful-booker.herokuapp.com/apidoc/index.html."""

    def __init__(self, username: str, password: str, endpoint: str):
        """HTTP клиент для работы с сервисом restful-booker.

        :param username: Логин.
        :param password: Пароль.
        :param endpoint: Адрес API сервиса.
        """
        self.username = username
        self.password = password
        self.endpoint = endpoint
        self.token = ''  # Авторизационный токен. Заполняется вызовом метода auth.

    def auth(self, username: str = None, password: str = None) -> Response:
        """Получение авторизационного токена.

        :param username: Логин.
        :param password: Пароль.
        :return: Объект ответа с авторизационным токеном в теле ответа.
        """
        body = {} | ({'username': username} if username else {}) | ({'password': password} if password else {})
        response = self.post(url=f'{self.endpoint}/auth', body=body, headers={Headers.CONTENT_TYPE: ContentType.JSON})
        if response.status_code == 200:
            self.token = response.json().get('token')
        return response

    def get_booking_ids(
            self,
            firstname: str = None,
            lastname: str = None,
            checkin: str = None,
            checkout: str = None
    ) -> Response:
        """Получение списка идентификаторов брони.

        :param firstname: Фильтр по имени.
        :param lastname: Фильтр по фамилии.
        :param checkin: Фильтр по дате заезда.
        :param checkout: Фильтр по дате выезда.
        :return: Объект ответа со списком идентификаторов имеющихся бронирований.
        """
        qerrystr = (
            '?' +
            (f'firstname={firstname}' if firstname else '') +
            (f'lastname={lastname}' if lastname else '') +
            (f'checkin={checkin}' if checkin else '') +
            (f'checkout={checkout}' if checkout else '')
        )
        return self.get(url=f'{self.endpoint}/booking' + (qerrystr if qerrystr != '?' else ''), headers={})

    def get_booking(self, booking_id: str | int, response_format: str = Accept.JSON) -> Response:
        """Получение данных по конкретной брони по её ID.

        :param booking_id: Идентификатор брони в виде целого числа (или его строкового представления).
        :param response_format: Формат в котором будут возвращены данные в ответе. Значение подставляется в
            отправляемый заголовок `Accept`. Возможные варианты: `application/json`, `application/xml`. По умолчанию -
            заголовок не передаётся в запросе, на уровне сервиса будет принято как `application/json`.
        :return: Объект ответа с данными запрашиваемой брони в теле.
        """
        return self.get(url=f'{self.endpoint}/booking/{booking_id}', headers={Headers.ACCEPT: response_format})

    def create_booking(
            self,
            booking: Booking,
            request_format: str = ContentType.JSON,
            response_format: str = Accept.JSON
    ) -> Response:
        """Создание брони.

        :param booking: Объект создаваемого бронирования.
        :param request_format: Формат в котором будут отправляться данные в запросе. Значение подставляется в
            отправляемый заголовок `Content-Type`. Возможные варианты: `application/json`, `text/xml`.
        :param response_format: Формат в котором будут возвращены данные в ответе. Значение подставляется в
            отправляемый заголовок `Accept`. Возможные варианты: `application/json`, `application/xml`.
        :return: Объект ответа с объектом созданной брони в теле.
        """
        headers = {Headers.ACCEPT: response_format, Headers.CONTENT_TYPE: request_format}
        return self.post(url=f'{self.endpoint}/booking', headers=headers, body=booking.output)

    def update_booking(  # pylint: disable=too-many-positional-arguments,too-many-arguments
            self,
            booking_id: str | int,
            new_booking: Booking,
            auth_type: str = 'basic',
            request_format: str = ContentType.JSON,
            response_format: str = Accept.JSON
    ) -> Response:
        """Полное обновление модели бронирования.

        :param booking_id: Идентификатор обновляемого бронирования.
        :param new_booking: Объект новых значений бронирования.
        :param auth_type: Тип авторизации. Возможные варианты: `token`, `basic`.
        :param request_format: Формат в котором будут отправляться данные в запросе. Значение подставляется в
            отправляемый заголовок `Content-Type`. Возможные варианты: `application/json`, `text/xml`.
        :param response_format: Формат в котором будут возвращены данные в ответе. Значение подставляется в
            отправляемый заголовок `Accept`. Возможные варианты: `application/json`, `application/xml`.
        :return: Объект ответа с объектом созданной брони в теле.
        """
        headers = {Headers.CONTENT_TYPE: request_format, Headers.ACCEPT: response_format}
        if auth_type == 'token':
            headers[Headers.COOKIE] = f'token={self.token}'
        else:
            token = b64encode(f"{self.username}:{self.password}".encode('utf-8')).decode("ascii")
            headers[Headers.AUTHORIZATION] = f'Basic {token}'
        return self.put(url=f'{self.endpoint}/booking/{booking_id}', body=new_booking.output, headers=headers)

    def partial_update_booking(  # pylint: disable=too-many-positional-arguments,too-many-arguments
            self,
            booking_id: str | int,
            new_booking: Dict[str, Any] | str,
            auth_type: str = 'basic',
            request_format: str = ContentType.JSON,
            response_format: str = Accept.JSON
    ) -> Response:
        """Частичное обновление модели бронирования.

        :param booking_id: Идентификатор обновляемого бронирования.
        :param new_booking: Объект новых значений бронирования. Часть модели Booking. Либо в виде словаря либо в виде
            XML строки.
        :param auth_type: Тип авторизации. Возможные варианты: `token`, `basic`.
        :param request_format: Формат в котором будут отправляться данные в запросе. Значение подставляется в
            отправляемый заголовок `Content-Type`. Возможные варианты: `application/json`, `text/xml`.
        :param response_format: Формат в котором будут возвращены данные в ответе. Значение подставляется в
            отправляемый заголовок `Accept`. Возможные варианты: `application/json`, `application/xml`.
        :return: Объект ответа с объектом созданной брони в теле.
        """
        headers = {Headers.CONTENT_TYPE: request_format, Headers.ACCEPT: response_format}
        if auth_type == 'token':
            headers[Headers.COOKIE] = f'token={self.token}'
        else:
            token = b64encode(f"{self.username}:{self.password}".encode('utf-8')).decode("ascii")
            headers[Headers.AUTHORIZATION] = f'Basic {token}'
        return self.patch(url=f'{self.endpoint}/booking/{booking_id}', body=new_booking, headers=headers)

    def delete_booking(self, booking_id: str | int, auth_type: str = 'basic') -> Response:
        """Удаление брони.

        :param booking_id: Идентификатор удаляемого бронирования.
        :param auth_type: Тип авторизации. Возможные варианты: `token`, `basic`.
        :return: Объект ответа без тела.
        """
        headers = {Headers.CONTENT_TYPE: ContentType.JSON}
        if auth_type == 'token':
            headers[Headers.COOKIE] = f'token={self.token}'
        else:
            token = b64encode(f"{self.username}:{self.password}".encode('utf-8')).decode("ascii")
            headers[Headers.AUTHORIZATION] = f'Basic {token}'
        return self.delete(url=f'{self.endpoint}/booking/{booking_id}', headers=headers)
