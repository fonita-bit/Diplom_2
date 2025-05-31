import allure
import requests
import pytest
from data.user_data import get_user
from utils.urls import URLS
from data.consts import USER_ALREADY_EXISTS, MISSING_FIELD_ERROR, INVALID_CREDENTIALS


@allure.title("Успешная регистрация нового пользователя")
def test_register_unique_user(register_user):
    # Пользователь зарегистрирован через фикстуру, можем проверить вход
    response = requests.post(URLS["login"], json={
        "email": register_user["email"], "password": register_user["password"]
    })
    assert response.status_code == 200
    assert response.json()["accessToken"]

@allure.title("Регистрация уже существующего пользователя")
def test_register_existing_user(register_user):
    response = requests.post(URLS["register"], json=register_user)
    assert response.status_code == 403
    assert response.json()["message"] == USER_ALREADY_EXISTS

@allure.title("Регистрация без обязательного поля")
@pytest.mark.parametrize("missing_field", ["email", "password", "name"])
def test_register_with_missing_field(missing_field):
    user = get_user()
    user.pop(missing_field)
    response = requests.post(URLS["register"], json=user)
    assert response.status_code in [400, 403]

@allure.title("Успешный логин")
def test_login_success(register_user):
    response = requests.post(URLS["login"], json={
        "email": register_user["email"], "password": register_user["password"]
    })
    assert response.status_code == 200
    assert response.json()["accessToken"]


@allure.title("Логин с неверными данными")
def test_login_invalid():
    response = requests.post(URLS["login"], json={"email": "wrong@test.com", "password": "123456"})
    assert response.status_code == 401


