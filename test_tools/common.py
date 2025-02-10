"""Разные переиспользуемые вспомогательные инструменты."""

import logging
from json import dumps
from logging import config, getLogger, Logger
from typing import Any

from allure import attach, attachment_type

from test_tools.constants.common import ROOT_PROJECT_PATH


def get_logger(name: str) -> Logger:
    """Настройка логера.

    :param name: Имя логера.
    :return: Логер.
    """
    logging.log_file_path = f'{ROOT_PROJECT_PATH}/log.log'
    config.fileConfig(f'{ROOT_PROJECT_PATH}/logging.conf')
    return getLogger(name)


def attach_json(obj: Any, name: str, prettify: bool = True):
    """Прикрепить объект к отчёту Allure с подсветкой синтаксиса и, если возможно, структурированием.

    :param obj: Объект для прикрепления.
    :param name: Имя вложения.
    :param prettify: Структурировать ли прикрепляемый объект (возможно только для сериализуемых в JSON объектов).
    """
    if isinstance(obj, dict | list):
        body = dumps(obj, ensure_ascii=False, indent=2 if prettify is True else None)
        attach(body=body, name=name, attachment_type=attachment_type.JSON)
    else:
        attach(body=obj, name=name, attachment_type=attachment_type.JSON)
