import json
from cryptography.fernet import Fernet
from django.conf import settings


class AccessToken:
    @classmethod
    def encrypt(cls, data):
        cipher = Fernet(settings.USER_ACCESS_TOKEN_SECRET_KEY)
        token_payload = json.dumps(data).encode()
        return cipher.encrypt(token_payload).decode()

    @classmethod
    def decrypt(cls, access_token):
        cipher = Fernet(settings.USER_ACCESS_TOKEN_SECRET_KEY)
        token_payload = cipher.decrypt(access_token.encode()).decode()
        return json.loads(token_payload)
