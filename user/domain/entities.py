import json

from cryptography.fernet import Fernet


class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @classmethod
    def convert_repo_model_to_entity(cls, repo_model):
        return cls(id=repo_model.id, username=repo_model.username)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def _get_token_info(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def generate_access_token(self, secret_key):
        token_info = self._get_token_info()
        encoded_token_info = json.dumps(token_info).encode()
        cipher = Fernet(secret_key)
        access_token = cipher.encrypt(encoded_token_info).decode()
        return access_token

    def check_access_token(self, access_token, secret_key):
        cipher = Fernet(secret_key)
        decrypt_token_info = cipher.decrypt(access_token.encode()).decode()
        decrypt_token_info = json.loads(decrypt_token_info)
        return decrypt_token_info == self._get_token_info()
