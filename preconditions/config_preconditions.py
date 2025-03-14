"""Предусловия связанные с конфигурированием тестов."""

from typing import Any, Dict

from allure import title
from pytest import fixture
from yaml import safe_load

from test_tools.constants.common import ROOT_PROJECT_PATH


@fixture(scope='session')
@title('Получены настройки окружения')
def setup_get_config() -> Dict[str, Any]:
    """Получение настроек окружения из файла config.yaml."""
    with open(f"{ROOT_PROJECT_PATH}/config.yaml", encoding='utf-8') as stream:
        return safe_load(stream=stream)
