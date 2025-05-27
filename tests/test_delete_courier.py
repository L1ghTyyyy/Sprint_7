import allure
from helpers import SamokatAPICourier
from conftest import login_courier, courier


@allure.feature("Удалить курьера")
class TestDeleteCourier:
    """Тесты на удаление курьера"""

    @allure.story("Тест: успешное удаление курьера")
    @allure.title("Тест: удаление существующего курьера")
    @allure.description("Генерируем данные курьера и удаляем его")
    def test_delete_courier_success(self, courier, login_courier):
        """Тест: удаление существующего курьера"""
        id_courier = login_courier
        response = courier.delete_request_delete_courier(id_courier)

        with allure.step("Проверка удаления курьера"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.SUCCESS_CODE
        assert response.json() == courier.DELETE_SUCCESS_JSON

    @allure.story("Тест: удаление несуществующего курьера")
    @allure.title("Тест: удаление несуществующего курьера")
    @allure.description("Генерируем данные несуществующего курьера и удаляем его")
    def test_delete_non_existing_courier(self, courier):
        """Тест: удаление несуществующего курьера"""
        id_courier = SamokatAPICourier.generate_random_courier_id()
        response = courier.delete_request_delete_courier(id_courier)

        with allure.step("Проверка удаления несуществующего курьера"):
            allure.attach(str(response.status_code), name="status_code")
            allure.attach(str(response.json()), name="text")

        assert response.status_code == courier.NOT_FOUND_CODE
        assert response.json()["message"] == courier.DELETE_NOT_FOUND_MESSAGE

# не покрыто "если отправить запрос без id, вернётся ошибка"
