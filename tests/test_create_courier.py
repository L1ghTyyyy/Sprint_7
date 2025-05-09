import pytest
import allure
from helpers import SamokatAPICourier
from conftest import create_new_courier, courier

MISSED_REGISTRATION_FIELDS = [
    {'login': 12},
    {'login': 12, 'password': ''},
    {'password': 12},
    {'login': '', 'password': 12}
]

CORRECT_REGISTRATION_FIELDS = [
    {'login': 15, 'password': 12, 'first_name': 12},
    {'login': 15, 'password': 12, 'first_name': ''},
    {'login': 15, 'password': 12}
]


@allure.feature("Создание курьера")
class TestCreateCourier:
    """Тесты на создание курьера"""

    @allure.story("Тест: успешная регистрация нового курьера")
    @allure.title("Тест для курьера: {registration_fields}")
    @allure.description("Генерируем данные для успешной регистрации курьера")
    @pytest.mark.parametrize("registration_fields", CORRECT_REGISTRATION_FIELDS)
    def test_create_new_courier_success(self, registration_fields, courier):
        """Тест: регистрация нового курьера"""
        courier.courier_data = registration_fields
        response = courier.post_request_create_courier()

        with allure.step("Проверка успешной регистрации нового курьера"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.CREATE_SUCCESS_CODE
        assert response.json() == courier.REGISTER_SUCCESS_JSON

    @allure.story("Тест: регистрация курьера с занятым логином")
    @allure.title("Тест: регистрация курьера с занятым логином")
    @allure.description("Создаем курьера, пробуем использовать его логин для другого курьера")
    def test_create_courier_busy_login(self, create_new_courier):
        """Тест: регистрация курьера с занятым логином"""
        common_login = create_new_courier[0]
        password = SamokatAPICourier.generate_courier_data()
        first_name = SamokatAPICourier.generate_courier_data()
        second_courier_data = {'login': common_login, 'password': password, 'first_name': first_name}

        second_courier = SamokatAPICourier()
        second_courier.courier_data = second_courier_data
        response = second_courier.post_request_create_courier()

        with allure.step("Проверка регистрации курьера с занятым логином"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == second_courier.CONFLICT_CODE
        assert response.json()["message"] == second_courier.REGISTER_CONFLICT_MESSAGE

    @allure.story("Тест: регистрация нового курьера с пропущенными полями")
    @allure.title("Тест для курьера: {registration_fields}")
    @allure.description("Генерируем данные регистрации курьера, получаем ошибку")
    @pytest.mark.parametrize("registration_fields", MISSED_REGISTRATION_FIELDS)
    def test_create_courier_missed_fields(self, courier, registration_fields):
        """Тест: регистрация нового курьера с пропущенными полями"""
        courier.courier_data = registration_fields
        response = courier.post_request_create_courier()

        with allure.step("Проверка регистрации курьера с пропущенными полями"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.UNFILLED_CODE
        assert response.json()["message"] == courier.REGISTER_UNFILLED_MESSAGE
