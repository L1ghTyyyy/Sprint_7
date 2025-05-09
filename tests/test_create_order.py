import pytest
import allure
from conftest import order


@allure.feature("Создание заказа")
class TestCreateOrder:
    """Тесты на создание заказа"""

    @allure.story("Тест: успешное создание заказа")
    @allure.title("Тест: создание заказа со скутером цвета {scooter_color_field}")
    @allure.description("Генерируем данные и создаем заказ")
    @pytest.mark.parametrize("scooter_color_field", [[], ["BLACK"], ["GREY"], ["GREY", "BLACK "]])
    def test_create_new_order_success(self, scooter_color_field, order):
        """Тест: успешное создание заказа"""
        order.set_scooter_color(scooter_color_field)
        response = order.post_request_create_orger()

        with allure.step("Проверка создания заказа"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == order.CREATE_SUCCESS_CODE
        assert "track" in response.json()
