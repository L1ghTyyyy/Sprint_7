import allure
from helpers import SamokatAPICourier
from conftest import login_courier, courier


@allure.feature("Список заказов")
class TestOrderList:
    """Тесты на получение списка заказов"""

    @allure.story("Тест: успешный запрос списка заказов")
    @allure.title("Тест: успешный запрос списка заказов")
    @allure.description("Генерируем данные курьера и получаем его список заказов")
    def test_get_order_list_success(self, courier, login_courier):
        """Тест: список заказов существующего курьера"""
        id_courier = login_courier
        response = courier.get_request_get_order_list(id_courier)

        with allure.step("Проверка извлечения списка заказов"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.SUCCESS_CODE
        assert "orders" in response.json()

    @allure.story("Тест: запрос списка заказов у несуществующего курьера")
    @allure.title("Тест: запрос списка заказов у несуществующего курьера")
    @allure.description("Получаем список заказов у несуществующего курьера")
    def test_get_order_list_non_existing_courier(self, courier):
        """Тест: список заказов несуществующего курьера"""
        id_courier = SamokatAPICourier.generate_random_courier_id()
        response = courier.get_request_get_order_list(id_courier)

        with allure.step("Проверка извлечения списка заказов несуществующего курьера"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.NOT_FOUND_CODE
        assert response.json()["message"] == courier.GET_ORDERS_NOT_FOUND_MESSAGE(id_courier)
