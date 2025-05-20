import allure
import requests
import pytest
from data.user_data import get_user
from utils.urls import URLS

@allure.title("Успешная регистрация нового пользователя")
def test_register_unique_user():
    user = get_user()
    response = requests.post(URLS["register"], json=user)
    assert response.status_code == 200
    assert response.json()["success"] is True

@allure.title("Регистрация уже существующего пользователя")
def test_register_existing_user():
    user = get_user()
    requests.post(URLS["register"], json=user)
    response = requests.post(URLS["register"], json=user)
    assert response.status_code == 403
    assert response.json()["message"] == "User already exists"

@allure.title("Регистрация без обязательного поля")
@pytest.mark.parametrize("missing_field", ["email", "password", "name"])
def test_register_with_missing_field(missing_field):
    user = get_user()
    user.pop(missing_field)
    response = requests.post(URLS["register"], json=user)
    assert response.status_code == 403 or response.status_code == 400

@allure.title("Успешный логин")
def test_login_success():
    user = get_user()
    requests.post(URLS["register"], json=user)
    response = requests.post(URLS["login"], json={"email": user["email"], "password": user["password"]})
    assert response.status_code == 200
    assert response.json()["accessToken"]

@allure.title("Логин с неверными данными")
def test_login_invalid():
    response = requests.post(URLS["login"], json={"email": "wrong@test.com", "password": "123456"})
    assert response.status_code == 401


