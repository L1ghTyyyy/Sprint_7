import requests
import json
import allure
from faker import Faker
import random
from .urls import URLs


class SamokatAPIOrder:
    HEADERS = {"Content-type": "application/json"}
    PAYLOAD_STRING = lambda self, request_data: json.dumps(request_data)

    SUCCESS_CODE = 200
    CREATE_SUCCESS_CODE = 201
    UNFILLED_CODE = 400
    NOT_FOUND_CODE = 404
    CONFLICT_CODE = 409

    GET_ID_UNFILLED_MESSAGE = "Недостаточно данных для поиска"
    GET_ID_NOT_FOUND_MESSAGE = "Заказ не найден"

    def __init__(self):
        fake = Faker()
        self._order_data = {
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'address': fake.street_name(),
            'metroStation': str(random.randint(1, 20)),
            'phone': fake.numerify('+7 ### ### ## ##'),
            'rentTime': str(random.randint(1, 8)),
            'deliveryDate': fake.date_between(start_date="today", end_date="+180d").strftime("%Y-%m-%d"),
            'comment': fake.sentence(),
            'color': []
        }

    def set_scooter_color(self, scooter_color):
        self._order_data['color'] = scooter_color

    @allure.step("Запрос на создание заказа")
    def post_request_create_orger(self):
        allure.attach(str(self._order_data), name="order_data")
        return requests.post(URLs.CREATE_ORDER_URL, data=self.PAYLOAD_STRING(self._order_data), headers=self.HEADERS)

    @allure.step("Запрос на извлечение информации о заказе")
    def get_request_get_order(self, track_order=None):
        params = {'t': track_order}
        return requests.get(URLs.TRACK_ORDER_URL, params=params)

    @staticmethod
    def generate_random_order_id():
        """Генерирует несуществующий id"""
        return random.randint(1_000_000, 9_999_999)
