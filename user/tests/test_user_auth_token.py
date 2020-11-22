import json
from django.conf import settings
from django.test import TestCase
from cryptography.fernet import Fernet

from user.domain.services import user_service
from user.token import AccessToken


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

    def test_check_access_token(self):
        repo_user = user_service.create_user(username='test1')
        token = AccessToken.obtain_access_token(repo_user)
        assert token
        assert AccessToken.get_user_by_access_token(token) == repo_user
