import allure
import requests
from data.user_data import get_user
from utils.urls import URLS

@allure.title("Изменение данных пользователя с авторизацией")
def test_change_user_with_auth():
    user = get_user()
    reg = requests.post(URLS["register"], json=user)
    token = reg.json()["accessToken"]
    headers = {"Authorization": token}
    new_name = {"name": "NewName"}
    response = requests.patch(URLS["user"], json=new_name, headers=headers)
    assert response.status_code == 200
    assert response.json()["user"]["name"] == "NewName"

@allure.title("Изменение данных пользователя без авторизации")
def test_change_user_no_auth():
    response = requests.patch(URLS["user"], json={"name": "Hacker"})
    assert response.status_code == 401
    assert response.json()["message"] == "You should be authorised"