"""Тесты на добавление новых пользователей."""

from uuid import uuid4

from allure import step, title, description, story, feature, link, epic

from test_tools.asserters import base_asserters


@epic('gRPC Example Service')
@feature('Пользователи')
@story('Добавление новых пользователей')
@link(url='https://github.com/ritchiesinger/grpc_example_service', name="gRPC Example Service")
class TestAddUsers:
    """Сценарии на добавление новых пользователей."""

    @title('Успешное добавление одного пользователя')
    @description('Позитивный сценарий добавления одного пользователя.')
    def test_add_user_success(self, setup_get_grpc_example_service_client, setup_users_cleanup_list):
        user_obj = {'login': f'test_add_user_success_{uuid4()}', 'email': 'richard@some.com', 'city': 'City'}
        with step('Добавление пользователя'):
            create_response = setup_get_grpc_example_service_client.add_users(users=[user_obj])
            result_obj = create_response['addResults'][0]
            base_asserters.assert_equal(expect='OK', actual=result_obj['responseMeta']['errorCode'], name='errorCode')
            setup_users_cleanup_list.append(result_obj['userInfo']['id'])
        with step('Получение данных созданного пользователя'):
            response = setup_get_grpc_example_service_client.get_user_by_login(login=user_obj['login'])
            base_asserters.assert_equal(expect='OK', actual=response['responseMeta']['errorCode'], name='errorCode')
            base_asserters.assert_equal(
                expect=result_obj['userInfo'],
                actual=response['userInfo'],
                allure_step_name='Полученные данные соответствуют ожиданию'
            )

    @title('Успешное добавление нескольких пользователей')
    @description('Позитивный сценарий добавления одного пользователя.')
    def test_add_several_users_success(self, setup_get_grpc_example_service_client, setup_users_cleanup_list):
        user_obj_1 = {'login': f'test_add_user_success_{uuid4()}', 'email': 'test@some.com', 'city': 'City'}
        user_obj_2 = {'login': f'test_add_user_success_{uuid4()}', 'email': 'test@some.com', 'city': 'City'}
        with step('Добавление нескольких пользователей'):
            create_response = setup_get_grpc_example_service_client.add_users(users=[user_obj_1, user_obj_2])
            _ = [  # Чтобы независимо от дальнейших проверок все успешно созданные пользователи удалились
                setup_users_cleanup_list.append(result['userInfo']['id'])
                for result in create_response['addResults'] if result['userInfo'].get('id')
            ]
            for result in create_response['addResults']:
                base_asserters.assert_equal(expect='OK', actual=result['responseMeta']['errorCode'], name='errorCode')
        with step('Получение данных Пользователя 1'):
            response = setup_get_grpc_example_service_client.get_user_by_login(login=user_obj_1['login'])
            base_asserters.assert_equal(expect='OK', actual=response['responseMeta']['errorCode'], name='errorCode')
            base_asserters.assert_equal(
                expect=create_response['addResults'][0]['userInfo'],
                actual=response['userInfo'],
                allure_step_name='Полученные данные соответствуют ожиданию'
            )
        with step('Получение данных Пользователя 2'):
            response = setup_get_grpc_example_service_client.get_user_by_login(login=user_obj_2['login'])
            base_asserters.assert_equal(expect='OK', actual=response['responseMeta']['errorCode'], name='errorCode')
            base_asserters.assert_equal(
                expect=create_response['addResults'][1]['userInfo'],
                actual=response['userInfo'],
                allure_step_name='Полученные данные соответствуют ожиданию'
            )

    @title('Частичный успех при добавлении нескольких пользователей')
    @description('Сценарий добавления нескольких пользователей, у одного из которых неуникальный логин.')
    def test_add_several_users_not_all_success(
            self,
            setup_get_grpc_example_service_client,
            setup_users_cleanup_list,
            setup_create_user_1
    ):
        exist_user = setup_create_user_1['addResults'][0]['userInfo']
        user_obj_1 = {'login': f'test_user_{uuid4()}', 'email': 'test@some.com', 'city': 'City'}
        user_obj_2 = {'login': exist_user['login'], 'email': 'test@some.com', 'city': 'City'}
        with step('Добавление нескольких пользователей'):
            create_response = setup_get_grpc_example_service_client.add_users(users=[user_obj_1, user_obj_2])
            _ = [  # Чтобы независимо от дальнейших проверок все успешно созданные пользователи удалились
                setup_users_cleanup_list.append(result['userInfo']['id'])
                for result in create_response['addResults'] if result['userInfo'].get('id')
            ]
            base_asserters.assert_equal(
                expect='OK',
                actual=create_response['addResults'][0]['responseMeta']['errorCode'],
                name='#1. errorCode'
            )
            base_asserters.assert_equal(
                expect='ALREADY_EXIST',
                actual=create_response['addResults'][1]['responseMeta']['errorCode'],
                name='#2. errorCode'
            )

    @title('Получение ошибки при добавлении пользователя с уже существующим логином')
    @description('Сценарий добавления пользователя с уже существующим в системе логином.')
    def test_add_user_already_exist_failed(
            self,
            setup_get_grpc_example_service_client,
            setup_create_user_1,
            setup_users_cleanup_list
    ):
        already_exist_user = setup_create_user_1['addResults'][0]['userInfo']
        user_obj = {'login': already_exist_user['login'], 'email': 'richard@some.com', 'city': 'City'}
        with step('Добавление пользователя'):
            create_response = setup_get_grpc_example_service_client.add_users(users=[user_obj])
            result_obj = create_response['addResults'][0]
            base_asserters.assert_equal(
                expect='ALREADY_EXIST',
                actual=result_obj['responseMeta']['errorCode'],
                name='errorCode'
            )
