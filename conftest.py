import pytest
import requests
from data.user_data import get_user
from utils.urls import URLS

@pytest.fixture
def register_user():
    user = get_user()
    # Регистрируем пользователя
    response = requests.post(URLS["register"], json=user)
    assert response.status_code == 200
    yield user  # Передаём пользователя в тест

    # После теста: удаляем пользователя
    token_resp = requests.post(URLS["login"], json={"email": user["email"], "password": user["password"]})
    if token_resp.status_code == 200:
        token = token_resp.json()["accessToken"]
        headers = {"Authorization": token}
        requests.delete(URLS["user"], headers=headers)  # URLS["user"] — должен вести на DELETE-эндпоинт удаления
