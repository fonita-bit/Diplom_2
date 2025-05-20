import random
import string

def random_email():
    return f"user_{''.join(random.choices(string.ascii_lowercase, k=8))}@test.com"

def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def get_user():
    return {
        "email": random_email(),
        "password": random_password(),
        "name": "TestUser"
    }
