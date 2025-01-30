"""Самописные асертеры. Сделаны чтобы не думать о том как будет отображаться в Allure."""

from typing import Any

from allure import step
from requests import Response


def assert_condition(condition: bool, allure_step_name: str, error_text: str):
    """Проверка истинности любого выражения.

    :param condition: Выражение, которое будет проверено на истинность.
    :param allure_step_name: Имя шага проверки в отчёте Allure.
    :param error_text: Текст ошибки в случае провала проверки.
    """
    with step(allure_step_name):
        assert condition is True, error_text


def assert_equal(expect: Any, actual: Any, allure_step_name: str = None, name: str = None, error_text: str = None):
    """Проверка равенства ожидаемого и фактического значения.

    :param expect: Ожидаемое значение.
    :param actual: Фактическое значение.
    :param allure_step_name: Имя шага проверки в отчёте Allure. Удобно для больших объектов.
    :param name: Имя проверяемого свойства. Удобно для маленьких объектов, когда можно в имя шага вывести значения.
    :param error_text: Текст ошибки в случае провала проверки.
    """
    step_name = (f'{name}. Ожидание: {expect}. Факт: {actual}' if name else allure_step_name) or f'{expect} == {actual}'
    error_text = error_text or f'Ожидаемое значение ({expect}) не равно фактическому ({actual})!'
    assert_condition(condition=expect == actual, allure_step_name=step_name, error_text=error_text)


def assert_status_code(expect: int, response: Response):
    """Проверка кода HTTP ответа.

    :param expect: Ожидаемый код ответа.
    :param response: Объект ответа.
    """
    msg = f'status_code. Ожидание: {expect}. Факт: {response.status_code}'
    assert_equal(expect=expect, actual=response.status_code, allure_step_name=msg, error_text=msg)
