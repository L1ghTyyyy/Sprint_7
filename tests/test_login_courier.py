import pytest
import allure
from helpers import SamokatAPICourier
from conftest import create_new_courier, courier

MISSED_LOGIN_FIELDS = [
    {'login': 12, 'password': ''},
    {'password': 12},
    {'login': '', 'password': 12}
]


@allure.feature("Логин курьера")
class TestLoginCourier:
    """Тесты на логин курьера"""

    @allure.story("Тест: успешный логин курьера")
    @allure.title("Тест: успешный логин курьера")
    @allure.description("Регистрируем и заходим в профиль курьера")
    def test_login_existing_courier_success(self, courier, create_new_courier):
        """Тест: успешный логин курьера"""
        login, password, first_name = create_new_courier
        response = courier.post_request_login_courier({'login': login, 'password': password})

        with allure.step("Проверка логина курьера"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.SUCCESS_CODE
        assert "id" in response.json()

    @allure.story("Тест: логин курьера с отсутствующими полями")
    @allure.title("Тест для курьера: {login_fields}")
    @allure.description("При попытке логина есть отсутствующие поля")
    @pytest.mark.parametrize("login_fields", MISSED_LOGIN_FIELDS)
    def test_login_courier_missed_fields(self, courier, login_fields):
        """Тест: логин курьера с пустыми полями"""
        response = courier.post_request_login_courier(login_fields)

        with allure.step("Проверка логина курьера с отсутствующими полями"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.UNFILLED_CODE
        assert response.json()["message"] == courier.LOGIN_UNFILLED_MESSAGE

    @allure.story("Тест: логин несуществующего курьера")
    @allure.title("Тест: логин несуществующего курьера")
    @allure.description("Попытка логина несуществующего курьера")
    def test_login_non_existing_courier(self, courier):
        """Тест: логин несуществующего курьера"""
        login = SamokatAPICourier.generate_courier_data()
        password = SamokatAPICourier.generate_courier_data()
        non_existing_courier_data = {'login': login, 'password': password}

        response = courier.post_request_login_courier(non_existing_courier_data)

        with allure.step("Проверка логина несуществующего курьера"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.NOT_FOUND_CODE
        assert response.json()["message"] == courier.LOGIN_NOT_FOUND_MESSAGE
