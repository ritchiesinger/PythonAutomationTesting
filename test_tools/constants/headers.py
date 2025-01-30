"""Константы для работы с заголовками HTTP запросов/ответов."""

from dataclasses import dataclass


@dataclass
class Headers:
    """Заголовки HTTP."""

    CONTENT_TYPE = 'Content-Type'
    ACCEPT = 'Accept'
    COOKIE = 'Cookie'
    AUTHORIZATION = 'Authorization'


@dataclass
class ContentType:
    """Формат данных отпраляемых в теле запроса. Значения заголовка Content-Type."""

    JSON = 'application/json'
    XML = 'text/xml'


@dataclass
class Accept:
    """Формат данных ожидаемый в теле ответа. Значения заголовка Accept."""

    JSON = 'application/json'
    XML = 'application/xml'
