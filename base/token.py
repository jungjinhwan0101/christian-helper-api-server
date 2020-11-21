import json
from cryptography.fernet import Fernet
from django.conf import settings


def encrypt_access_token(plain_data):
    cipher = Fernet(settings.USER_ACCESS_TOKEN_SECRET_KEY)
    token_payload = json.dumps(plain_data).encode()
    return cipher.encrypt(token_payload).decode()


def decrypt_access_token(encrypted_token):
    cipher = Fernet(settings.USER_ACCESS_TOKEN_SECRET_KEY)
    token_payload = cipher.decrypt(encrypted_token.encode()).decode()
    return json.loads(token_payload)
