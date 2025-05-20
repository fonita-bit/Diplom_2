import allure
import requests
import pytest
from data.user_data import get_user
from utils.urls import URLS

@allure.title("Создание заказа с авторизацией и ингредиентами")
def test_create_order_with_auth():
    user = get_user()
    reg = requests.post(URLS["register"], json=user)
    token = reg.json()["accessToken"]
    headers = {"Authorization": token}
    ingredients = {"ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa72"]}  # пример хешей
    response = requests.post(URLS["orders"], json=ingredients, headers=headers)
    assert response.status_code == 200
    assert response.json()["order"]

@allure.title("Создание заказа без ингредиентов")
def test_create_order_no_ingredients():
    user = get_user()
    reg = requests.post(URLS["register"], json=user)
    token = reg.json()["accessToken"]
    headers = {"Authorization": token}
    response = requests.post(URLS["orders"], json={}, headers=headers)
    assert response.status_code == 400
    assert "message" in response.json()

@allure.title("Создание заказа без авторизации")
def test_create_order_no_auth():
    ingredients = {"ingredients": ["61c0c5a71d1f82001bdaaa6d"]}
    response = requests.post(URLS["orders"], json=ingredients)
    assert response.status_code == 200  # в API допускается создание заказа без авторизации

@allure.title("Получение заказов авторизованного пользователя")
def test_get_user_orders_auth():
    user = get_user()
    reg = requests.post(URLS["register"], json=user)
    token = reg.json()["accessToken"]
    headers = {"Authorization": token}
    response = requests.get(URLS["orders"], headers=headers)
    assert response.status_code == 200
    assert "orders" in response.json()

@allure.title("Получение заказов неавторизованного пользователя")
def test_get_user_orders_no_auth():
    response = requests.get(URLS["orders"])
    assert response.status_code == 401
    assert response.json()["message"] == "You should be authorised"
