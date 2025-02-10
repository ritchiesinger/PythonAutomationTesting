"""Конструкторы объектов учебного GRPC сервиса."""


class ClientInfo(dict):
    """Данные клиента."""

    def __init__(self, city: str, login: str, email: str):
        """Данные клиента.

        :param city: Город.
        :param login: Логин.
        :param email: Электронная почта.
        """
        self.city = city
        self.login = login
        self.email = email
        super().__init__({'city': city, 'login': login, 'email': email})
