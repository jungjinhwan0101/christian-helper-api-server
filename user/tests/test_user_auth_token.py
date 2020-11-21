import json
from django.conf import settings
from django.test import TestCase
from cryptography.fernet import Fernet

from user.domain.entities import User
from user.domain.factories import UserServiceFactory


class UserAuthTokenTest(TestCase):
    def test_token(self):
        cipher_suite = Fernet(settings.USER_ACCESS_TOKEN_SECRET_KEY)
        data = {
            'id': 1,
            'data': {
                'data1': 0,
                'data2': ['1'],
            },
            'data3': 'test',
        }
        encoded_data = json.dumps(data).encode()
        cipher_data = cipher_suite.encrypt(encoded_data)
        print("encrypt_data: ", cipher_data)

        plain_data = cipher_suite.decrypt(cipher_data)
        decoded_data = plain_data.decode()
        print("decrypt_data: ", json.loads(decoded_data))

        assert json.loads(decoded_data) == data

        # encrypt 의 암호화시, 현재시간에 대한 값도 함께 포함되어 있어서 토큰값은 매번 다른값으로 반환됨
        cipher_data2 = cipher_suite.encrypt(encoded_data)
        assert encoded_data != cipher_data2

        plain_data2 = cipher_suite.decrypt(cipher_data2)
        decoded_data2 = plain_data2.decode()
        
        # 복호화 된 데이터 체크
        assert json.loads(decoded_data) == json.loads(decoded_data2) == data

    def test_user_service_get_access_token(self):
        user_service = UserServiceFactory.get()
        repo_user = user_service.create_user(username='test1')
        user_entity = User.convert_repo_model_to_entity(repo_user)
        token = user_entity.generate_access_token(secret_key=settings.USER_ACCESS_TOKEN_SECRET_KEY)
        assert token
        assert user_entity.check_access_token(token, secret_key=settings.USER_ACCESS_TOKEN_SECRET_KEY) is True
        user_entity.id = 2
        assert user_entity.check_access_token(token, secret_key=settings.USER_ACCESS_TOKEN_SECRET_KEY) is False
        user_entity.id = 1
        assert user_entity.check_access_token(token, secret_key=settings.USER_ACCESS_TOKEN_SECRET_KEY) is True
        user_entity.username = 'test2'
        assert user_entity.check_access_token(token, secret_key=settings.USER_ACCESS_TOKEN_SECRET_KEY) is False
        user_entity.username = 'test1'
        assert user_entity.check_access_token(token, secret_key=settings.USER_ACCESS_TOKEN_SECRET_KEY) is True
