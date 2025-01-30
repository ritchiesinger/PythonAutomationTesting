"""Базовый HTTP клиент. От него наследуем HTTP клиенты конкретных сервисов."""

from json import dumps
from logging import config, getLogger
from typing import Any, Dict

from allure import attach, attachment_type
from requests import Request, Response, Session, exceptions

config.fileConfig('logging.conf')
logger = getLogger('http_client')
REQUEST_LOG_TEMPLATE = 'URL ЗАПРОСА: %s %s\n    ЗАГОЛОВКИ: %s\n    ТЕЛО ЗАПРОСА: %s'
RESPONSE_LOG_TEMPLATE = 'КОД ОТВЕТА: %s\n    ЗАГОЛОВКИ: %s\n    ТЕЛО ОТВЕТА: %s'
ALLURE_REQUEST_ATTACH_TEMPLATE = 'URL ЗАПРОСА: %s %s\nЗАГОЛОВКИ: %s\nТЕЛО ЗАПРОСА: %s'
ALLURE_RESPONSE_ATTACH_TEMPLATE = 'КОД ОТВЕТА: %s\nЗАГОЛОВКИ: %s\nТЕЛО ОТВЕТА: %s'


def log_request(func):
    """Декоратор для логирования запросов и вложений в Allure."""
    def wrapper(*args, **kwargs):
        ro: Request = kwargs.get('request_obj') or [item for item in args if isinstance(item, Request)][0]
        logger.debug(REQUEST_LOG_TEMPLATE, ro.method, ro.url, ro.headers, ro.json or ro.data)
        allure_attach_str = ALLURE_REQUEST_ATTACH_TEMPLATE % (
            ro.method,
            ro.url,
            ro.headers,
            dumps(ro.json, ensure_ascii=False, indent=2)
        ) if ro.json else ALLURE_REQUEST_ATTACH_TEMPLATE % (ro.method, ro.url, ro.headers, ro.data)
        original_result: Response = func(*args, **kwargs)
        try:
            response_data = original_result.json()
            allure_attach_str += '\n\n' + ALLURE_RESPONSE_ATTACH_TEMPLATE % (
                original_result.status_code,
                dumps(dict(original_result.headers), ensure_ascii=False, indent=2),
                dumps(original_result.json(), ensure_ascii=False, indent=2)
            )
        except exceptions.JSONDecodeError:
            response_data = original_result.content
            allure_attach_str += '\n\n' + ALLURE_RESPONSE_ATTACH_TEMPLATE % (
                original_result.status_code,
                dumps(dict(original_result.headers), ensure_ascii=False, indent=2),
                str(response_data)
            )
        attach(body=allure_attach_str, name=f'{ro.method} {ro.url}', attachment_type=attachment_type.JSON)
        logger.debug(RESPONSE_LOG_TEMPLATE, original_result.status_code, original_result.headers, response_data)
        return original_result
    return wrapper


class HTTPClient:
    """Базовый класс для всех HTTP клиентов."""

    DEFAULT_HEADERS = {}  # Возможность задать дефолтные заголовки индивидуально для каждого потомка (сервиса).

    @log_request
    def send(self, request_obj: Request) -> Response:
        """Подготовка и отправка запроса. Работает с нативными объектами запроса/ответа из библиотеки requests.

        :param request_obj: Объект запроса, который будет подготовлен и отправлен.
        :return: Объект ответа.
        """
        session = Session()
        req = request_obj.prepare()
        return session.send(request=req)

    def get(self, url, headers: Dict[str, Any] = None, extra_headers: Dict[str, Any] = None) -> Response:
        """Отправка GET запроса.

        :param url: Полный адрес отправки запроса, включая querystring.
        :param headers: Возможность явно указать абсолютный набор заголовков запроса
            (что передано, то и будет отправлено).
        :param extra_headers: Возможность дополнить абсолютный (или дефолтный) набор заголовков.
        :return: Объект ответа.
        """
        headers = headers if headers is not None else self.DEFAULT_HEADERS
        if extra_headers:
            headers.update(extra_headers)
        return self.send(Request(method='GET', url=url, headers=headers))

    def post(
            self,
            url,
            body: Dict[str, any] | str = None,
            headers: Dict[str, Any] = None,
            extra_headers: Dict[str, Any] = None
    ) -> Response:
        """Отправка POST запроса.

        :param url: Полный адрес отправки запроса, включая querystring.
        :param body: Тело запроса. Если передан словарь - приводится к JSON, иначе отправляется как есть.
        :param headers: Возможность явно указать абсолютный набор заголовков запроса
            (что передано, то и будет отправлено).
        :param extra_headers: Возможность дополнить абсолютный (или дефолтный) набор заголовков.
        :return: Объект ответа.
        """
        headers = headers or self.DEFAULT_HEADERS
        body = dumps(body) if isinstance(body, dict) else body
        if extra_headers:
            headers.update(extra_headers)
        return self.send(Request(method='POST', url=url, headers=headers, data=body))

    def put(
            self,
            url,
            body: Dict[str, any] | str = None,
            headers: Dict[str, Any] = None,
            extra_headers: Dict[str, Any] = None
    ) -> Response:
        """Отправка PUT запроса.

        :param url: Полный адрес отправки запроса, включая querystring.
        :param body: Тело запроса. Если передан словарь - приводится к JSON, иначе отправляется как есть.
        :param headers: Возможность явно указать абсолютный набор заголовков запроса
            (что передано, то и будет отправлено).
        :param extra_headers: Возможность дополнить абсолютный (или дефолтный) набор заголовков.
        :return: Объект ответа.
        """
        headers = headers or self.DEFAULT_HEADERS
        body = dumps(body) if isinstance(body, dict) else body
        if extra_headers:
            headers.update(extra_headers)
        return self.send(Request(method='PUT', url=url, headers=headers, data=body))

    def patch(
            self,
            url,
            body: Dict[str, any] | str = None,
            headers: Dict[str, Any] = None,
            extra_headers: Dict[str, Any] = None
    ) -> Response:
        """Отправка PATCH запроса.

        :param url: Полный адрес отправки запроса, включая querystring.
        :param body: Тело запроса. Если передан словарь - приводится к JSON, иначе отправляется как есть.
        :param headers: Возможность явно указать абсолютный набор заголовков запроса
            (что передано, то и будет отправлено).
        :param extra_headers: Возможность дополнить абсолютный (или дефолтный) набор заголовков.
        :return: Объект ответа.
        """
        headers = headers or self.DEFAULT_HEADERS
        body = dumps(body) if isinstance(body, dict) else body
        if extra_headers:
            headers.update(extra_headers)
        return self.send(Request(method='PATCH', url=url, headers=headers, data=body))

    def delete(self, url, headers: Dict[str, Any] = None, extra_headers: Dict[str, Any] = None) -> Response:
        """Отправка DELETE запроса.

        :param url: Полный адрес отправки запроса, включая querystring.
        :param headers: Возможность явно указать абсолютный набор заголовков запроса
            (что передано, то и будет отправлено).
        :param extra_headers: Возможность дополнить абсолютный (или дефолтный) набор заголовков.
        :return: Объект ответа.
        """
        headers = headers or self.DEFAULT_HEADERS
        if extra_headers:
            headers.update(extra_headers)
        return self.send(Request(method='DELETE', url=url, headers=headers))
