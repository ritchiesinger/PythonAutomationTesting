"""Конструктор объекта бронирования."""

from json import dumps


class Booking(dict):  # pylint: disable=too-many-instance-attributes
    """Бронирование."""

    def __init__(  # pylint: disable=too-many-positional-arguments,too-many-arguments
            self,
            firstname: str,
            lastname: str,
            totalprice: int,
            depositpaid: bool,
            checkin: str,
            checkout: str,
            additionalneeds: str
    ):
        """Бронирование.

        :param firstname: Имя.
        :param lastname: Фамилия.
        :param totalprice: Суммарная стоимость.
        :param depositpaid: Внесён ли депозит.
        :param checkin: Дата въезда.
        :param checkout: Дата выезда.
        :param additionalneeds: Дополнительные пожелания.
        """
        self.output = ''  # Представление объекта для запроса (XML или JSON).
        self.firstname = firstname
        self.lastname = lastname
        self.totalprice = totalprice
        self.depositpaid = depositpaid
        self.checkin = checkin
        self.checkout = checkout
        self.additionalneeds = additionalneeds
        super().__init__({
            'firstname': firstname,
            'lastname': lastname,
            'totalprice': totalprice,
            'depositpaid': depositpaid,
            'bookingdates': {'checkin': checkin, 'checkout': checkout},
            'additionalneeds': additionalneeds
        })

    def to_json(self):
        """Приведение объекта к строке JSON и запись результата в свойство output в виде строки."""
        self.output = dumps(self)
        return self

    def to_xml(self):
        """Приведение объекта к строке XML и запись результата в свойство output в виде строки."""
        self.output = ''
        return self
