"""Инструмент для множественной "мягкой" проверки для случаев когда требуется провести все проверки, не падая на первой
же проваленной.

Пример использования:
SoftAssert(
    base_asserters.assert_equal(expect=0, actual=0, name='Целочисленное сравнение (успех 1)', soft_assert=True),
    base_asserters.assert_equal(expect=0, actual=1, name='Целочисленное сравнение (провал)', soft_assert=True),
    base_asserters.assert_equal(expect=0, actual=0, name='Целочисленное сравнение (успех 2)', soft_assert=True),
    base_asserters.assert_equal(expect=0, actual=0, name='Целочисленное сравнение (успех 3)', soft_assert=True),
)
В этом случае выполнятся все 4 проверки и будет выведено сообщение о том сколько проверок успешно, а сколько провалено
с соответствующими error_msg.
"""


class SoftAssert:  # pylint: disable=too-few-public-methods  # Публичных методов пока не предполагается.
    """Для массовых проверок в случаях когда требуется провести все проверки, не падая на первой же проваленной."""

    def __init__(self, *checks, error_msg: str = 'Одна или более проверок провалились!'):
        """Для массовых проверок в случаях когда требуется провести все проверки, не падая на первой же проваленной.

        :param checks: Кастомные асертеры (base_asserters), позицонно переданные в иницилизатор с параметром
            soft_assert = True.
        :param error_msg: Возможность настроить уникальное сообщение об ошибке, дающее дополнительные сведения в
            случае падений одной из проверок.
        """
        checks = checks or []
        error_list = []
        for check in checks:
            try:
                check()
            except AssertionError as err:
                error_list.append(str(err))
            except Exception as err:
                raise Exception(f'Необрабатываемая ошибка! {err}') from err  # pylint: disable=broad-exception-raised
        if error_list:
            err_msgs = '    ' + '\n    '.join(error_list)
            raise AssertionError(f'{error_msg}\nПроваленные проверки ({len(error_list)} из {len(checks)}):\n{err_msgs}')
