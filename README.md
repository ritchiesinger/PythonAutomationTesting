# REST API Python Automation Testing

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

## Описание

Проект задуман для нескольких целей:
- Учебное пособие по автоматизации тестирования на `Python`.
- Универсальный шаблон для проектирования фреймворка автоматизации тестирования.
- Источник живых (не абстрактных) примеров кода и отчётов о прогоне автотестов.

На протяжении более чем 10-летнего опыта в сфере тестирования ПО приходилось 
регулярно изобретать велосипеды и при смене работы зачастую воспроизводить 
собственные идеи повторно.

И в какой-то момент захотелось где-то иметь базу знаний с лучшими наработками. 
По понятным причинам прямое цитирование не представлялось возможным. Поэтому я 
нашёл открытый API и решил создать этот репозиторий.

На момент написания в проекте реализованы автотесты для открытого учебного 
сервиса Restful-Booker. Причём ценность здесь не сколько в конкретном сервисе, 
а в том, что реализованы вспомогательные инструменты и переиспользуя их можно 
достаточно быстро реализовывать автотесты любого другого сервиса.

В планах - для демонстрации универсальности подхода - сделать тесты ещё для 
пары-тройки сервисов с `REST API`. Также не ограничиваться только `HTTP` 
тестами. Если найдутся сервисы с открытыми программными интерфейсами 
`GRPC`, `SOAP` - уделим время и силы и этим направлениям. Автоматизацию 
тестирования фронта (`WEB UI`) тоже вероятно не обойдём стороной: 
`Selenium`, `Playwright`.

## Требования

Код проекта писался на `Python 3.12`, но насколько я могу судить - я не 
использую каких-то "современных" конструкций языка, и смею предположить 
что код будет работать на `Python 3.8` (а может и более ранних, я не пробовал). 
Другое дело что все зависимости проекта (см. `requirements.txt`) имеют жёстко
зафиксированную версию, а это значит что вероятно на ранних версиях языка они 
просто могут не установиться.

## Установка

После стягивания репозитория:
- Создаём `venv` с `Python 3.12`.
- Активируем `venv` и устанавливаем зависимости: 
```bash
pip install -r requirements.txt
```
Кроме того потребуется установить [Allure Reports](https://allurereport.org/docs/install/) 
и настроить переменные окружения чтобы из любого места системы можно было вызывать 
команду `allure`.

Всё. Можно запускать тесты. В корневой папке проекта:
```bash
pytest --alluredir allure_reports
```

После прохождения тестов исходники для отчёта будут в папке `allure_reports` 
в корне проекта. Для генерации отчёта (в корне проекта):
```bash
allure serve allure_reports
```

## Подробнее о том как сделано

### Структура проекта
 
| - - preconditions  
| - - test_tools  
| - - - - asserters  
| - - - - clients  
| - - - - constants  
| - - - - objects  
| - - - - waiters  
| - - tests  
| `.pylintrc` - файл-конфиг для линтера `pylint`.  
| `conftest.py` - файл-конфиг для тестов (регистрация фикстур, хуки и т.д)  
| `logging.conf` - файл-конфиг логера.  
| `pytest.ini` - файл-конфиг для `Pytest`.  
| `README.md` - документ который ты сейчас читаешь.  
| `requirements.txt` - список зависимостей проекта.  
| `requirements-dev.txt` - список технических зависимостей проекта, которые 
напрямую не влияют на работу тестов (линтеры, например, там).

#### preconditions

Здесь лежат фикстуры `Pytest` семантически разделённые по модулям. 
Каждый модуль нужно "зарегистрировать" в корневом `conftest.py` в 
переменной `pytest_plugins` чтобы тесты видели фикстуры из него.

#### test_tools

Всё вспомогательное, что нужно для того чтобы тесты не выглядели 
монструозными франкенштейнами. Как только возникает мысль о 
реализации чего-то переиспользуемого - кладём это здесь.

##### asserters

Самописные асертеры. Основная причина их писать - чтобы не думать 
о том как это будет отображаться в отчёте.

##### clients

Клиенты (как базовые, так и наследники) для работы с сервисами.

##### constants

Один из вариантов хранения констант - выделение своей папки 
(пакета) под них.

##### objects

Для тех кто любит самописные объекты, а также такие слова как 
"Композиция" в ООП - надо выделить под это своё место.

##### waiters

Всегда есть что-то асинхронное и потребность организовывать 
ожидание какого-то события. Хороший подход - сделать набор 
целевых ожидалок. И выделить под них место в структуре проекта.

#### tests

Собственно тесты.

### Логирование

- {написать как настроено}

### Линтеры

К проекту прикручен самый распространённый линтер - `Pylint`. 

Настроен для него конфиг - `.pylintrc` - лежит в корне проекта. 
