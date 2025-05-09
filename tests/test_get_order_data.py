import allure
from helpers import SamokatAPIOrder
from conftest import create_new_order, order


@allure.feature("Получить заказ")
class TestGetOrderData:
    """Тесты на извлечение информации о заказе"""

    @allure.story("Тест: успешное извлечение информации о заказе")
    @allure.title("Тест: успешное извлечение информации о заказе")
    @allure.description("Генерируем данные заказа и запрашиваем данные")
    def test_get_order_data_success(self, order, create_new_order):
        """Тест: успешное извлечение информации о заказе"""
        track_order = create_new_order
        response = order.get_request_get_order(track_order)

        with allure.step("Проверка получения заказа"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == order.SUCCESS_CODE
        assert "order" in response.json()

    @allure.story("Тест: извлечение информации без номера заказа")
    @allure.title("Тест: извлечение информации без номера заказа")
    @allure.description("Запрашиваем данные без номера заказа")
    def test_get_order_data_wo_number(self, order):
        """Тест: извлечение информации без номера заказа"""
        response = order.get_request_get_order()

        with allure.step("Проверка ошибки"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == order.UNFILLED_CODE
        assert response.json()["message"] == order.GET_ID_UNFILLED_MESSAGE

    @allure.story("Тест: запрос данных несуществующего заказа")
    @allure.title("Тест: запрос данных несуществующего заказа")
    @allure.description("Запрашиваем данные несуществующего заказа")
    def test_get_order_data_non_existing_number(self, order):
        """Тест: запрос данных несуществующего заказа"""
        track_order = SamokatAPIOrder.generate_random_order_id()
        response = order.get_request_get_order(track_order)

        with allure.step("Проверка ошибки"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == order.NOT_FOUND_CODE
        assert response.json()["message"] == order.GET_ID_NOT_FOUND_MESSAGE
