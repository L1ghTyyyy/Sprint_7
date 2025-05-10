import requests
import json
import allure
import random
import string
from .urls import URLs


class SamokatAPICourier:
    HEADERS = {"Content-type": "application/json"}
    PAYLOAD_STRING = lambda self, request_data: json.dumps(request_data)

    SUCCESS_CODE = 200
    CREATE_SUCCESS_CODE = 201
    UNFILLED_CODE = 400
    NOT_FOUND_CODE = 404
    CONFLICT_CODE = 409

    REGISTER_SUCCESS_JSON = {"ok": True}
    REGISTER_CONFLICT_MESSAGE = "Этот логин уже используется. Попробуйте другой."
    REGISTER_UNFILLED_MESSAGE = "Недостаточно данных для создания учетной записи"

    LOGIN_NOT_FOUND_MESSAGE = "Учетная запись не найдена"
    LOGIN_UNFILLED_MESSAGE = "Недостаточно данных для входа"

    DELETE_SUCCESS_JSON = {"ok": True}
    DELETE_NOT_FOUND_MESSAGE = "Курьера с таким id нет."

    GET_ORDERS_NOT_FOUND_MESSAGE = lambda self, id_courier: f"Курьер с идентификатором {id_courier} не найден"

    ACCEPT_ORDER_SUCCESS_JSON = {"ok": True}
    ACCEPT_ORDER_UNFILLED_MESSAGE = "Недостаточно данных для поиска"
    ACCEPT_ORDER_NOT_FOUND_ORDER_MESSAGE = "Заказа с таким id не существует"
    ACCEPT_ORDER_NOT_FOUND_COURIER_MESSAGE = "Курьера с таким id не существует"
    ACCEPT_ORDER_CONFLICT_MESSAGE = "Этот заказ уже в работе"

    def __init__(self):
        self._courier_data = {}

    def delete_courier(self, courier_id):
        """Удаляет курьера по ID"""
        return requests.delete(
            f"https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}"
        )

    @property
    def courier_data(self):
        return self._courier_data

    @courier_data.setter
    def courier_data(self, data):
        for k, v in data.items():
            self._courier_data[k] = v if not type(v) is int else self.generate_courier_data(v)

    @allure.step("Запрос на создание нового курьера")
    def post_request_create_courier(self):
        allure.attach(str(self._courier_data), name="courier_data")
        return requests.post(URLs.CREATE_COURIER_URL, data=self.PAYLOAD_STRING(self._courier_data),
                             headers=self.HEADERS)

    @allure.step("Запрос на логин курьера")
    def post_request_login_courier(self, request_data):
        return requests.post(URLs.LOGIN_COURIER_URL, data=self.PAYLOAD_STRING(request_data), headers=self.HEADERS)

    @allure.step("Запрос на удаление курьера")
    def delete_request_delete_courier(self, id_courier):
        url = URLs.DELETE_COURIER_URL + str(id_courier)
        return requests.delete(url)

    @allure.step("Запрос списка заказов")
    def get_request_get_order_list(self, id_courier=None):
        params = {'courierId': id_courier}
        return requests.get(URLs.ORDER_LIST_URL, params=params)

    @allure.step("Запрос на принятие заказа")
    def put_request_accept_order(self, id_order, id_courier=None):
        params = {'courierId': id_courier}
        url = URLs.ACCEPT_ORDER_URL + str(id_order)
        return requests.put(url, params=params)

    @staticmethod
    def generate_courier_data(length=12):
        """Генерирует случайную строку из букв и цифр."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    @staticmethod
    def generate_random_courier_id():
        """Генерирует несуществующий id"""
        return random.randint(1_000_000, 9_999_999)
