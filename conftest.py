import pytest
from helpers import SamokatAPICourier, SamokatAPIOrder


@pytest.fixture
def courier():
    return SamokatAPICourier()


@pytest.fixture
def create_new_courier(courier):
    """Фикстура для регистрации и удаления курьера"""
    login = SamokatAPICourier.generate_courier_data()
    password = SamokatAPICourier.generate_courier_data()
    first_name = SamokatAPICourier.generate_courier_data()
    courier_data = {'login': login, 'password': password, 'first_name': first_name}

    courier.courier_data = courier_data
    courier.post_request_create_courier()

    yield login, password, first_name

    courier_id = courier.post_request_login_courier({'login': login, 'password': password}).json().get("id")
    if courier_id:
        courier.delete_request_delete_courier(courier_id)


@pytest.fixture
def login_courier(courier, create_new_courier):
    """Фикстура для логина курьера в системе"""
    login, password, first_name = create_new_courier

    courier_data = {'login': login, 'password': password}
    response = courier.post_request_login_courier(courier_data)

    return response.json()["id"]


@pytest.fixture
def order():
    return SamokatAPIOrder()


@pytest.fixture
def create_new_order(order):
    """Фикстура для создания заказа"""
    response = order.post_request_create_orger()

    return response.json()["track"]
