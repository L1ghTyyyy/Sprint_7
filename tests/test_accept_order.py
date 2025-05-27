import allure
from helpers import SamokatAPIOrder, SamokatAPICourier
from conftest import login_courier, create_new_order, courier, order


@allure.feature("Принять заказ")
class TestAcceptOrder:
    """Тесты на принятие заказа"""

    @allure.story("Тест: успешное принятие заказа")
    @allure.title("Тест: успешное принятие заказа")
    @allure.description("Генерируем данные курьера и заказа, принимаем заказ")
    def test_accept_order_success(self, courier, login_courier, order, create_new_order):
        """Тест: успешное принятие заказа"""
        id_courier = login_courier
        track_order = create_new_order
        order_response = order.get_request_get_order(track_order)
        id_order = order_response.json()["order"]["id"]

        response = courier.put_request_accept_order(id_order, id_courier)

        with allure.step("Проверка подтверждения заказа"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.SUCCESS_CODE
        assert response.json() == courier.ACCEPT_ORDER_SUCCESS_JSON

    @allure.story("Тест: принять заказ с запросом без номера курьера")
    @allure.title("Тест: принять заказ с запросом без номера курьера")
    @allure.description("Генерируем данные заказа, пробуем принять заказ без номера курьера")
    def test_accept_order_missed_courier_number(self, courier):
        """Тест: принять заказ с запросом без номера"""
        id_order = SamokatAPIOrder.generate_random_order_id()
        response = courier.put_request_accept_order(id_order)

        with allure.step("Проверка ошибки из-за отсутствия номера"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.UNFILLED_CODE
        assert response.json()["message"] == courier.ACCEPT_ORDER_UNFILLED_MESSAGE

    @allure.story("Тест: принять заказ с несуществующим номером")
    @allure.title("Тест: принять заказ с несуществующим номером")
    @allure.description("Генерируем данные заказа и курьера, пробуем принять заказ с несуществующим номером")
    def test_accept_order_non_existing_number(self, courier, login_courier):
        """Тест: принять заказ с несуществующим номером"""
        id_order = SamokatAPIOrder.generate_random_order_id()
        id_courier = login_courier
        response = courier.put_request_accept_order(id_order, id_courier)

        with allure.step("Проверка ошибки из-за несуществующего номера"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.NOT_FOUND_CODE
        assert response.json()["message"] == courier.ACCEPT_ORDER_NOT_FOUND_ORDER_MESSAGE

    @allure.story("Тест: принять заказ с несуществующим номером курьера")
    @allure.title("Тест: принять заказ с несуществующим номером курьера")
    @allure.description("Генерируем данные заказа и курьера, пробуем принять заказ с несуществующим номером курьера")
    def test_accept_order_non_existing_courier(self, order, create_new_order, courier):
        """Тест: принять заказ с несуществующим номером курьера"""
        id_courier = SamokatAPICourier.generate_random_courier_id()
        track_order = create_new_order
        order_response = order.get_request_get_order(track_order)
        id_order = order_response.json()["order"]["id"]

        response = courier.put_request_accept_order(id_order, id_courier)

        with allure.step("Проверка ошибки из-за несуществующего номера"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.NOT_FOUND_CODE
        assert response.json()["message"] == courier.ACCEPT_ORDER_NOT_FOUND_COURIER_MESSAGE

    @allure.story("Тест: принять занятый заказ повторно")
    @allure.title("Тест: принять занятый заказ повторно")
    @allure.description("Генерируем данные курьера и заказа, принимаем заказ")
    def test_accept_order_double_accept(self, courier, login_courier, order, create_new_order):
        """Тест: принять занятый заказ повторно"""
        id_courier = login_courier
        track_order = create_new_order
        order_response = order.get_request_get_order(track_order)
        id_order = order_response.json()["order"]["id"]

        # первый раз принимаем заказ
        accept_order = courier.put_request_accept_order(id_order, id_courier)
        # второй раз принимаем заказ
        response = courier.put_request_accept_order(id_order, id_courier)

        with allure.step("Проверка подтверждения заказа"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.CONFLICT_CODE
        assert response.json()["message"] == courier.ACCEPT_ORDER_CONFLICT_MESSAGE

# не покрыто "если не передать id заказа, запрос вернёт ошибку"
