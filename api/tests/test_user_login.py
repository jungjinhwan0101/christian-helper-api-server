from django.test import TestCase

from user.domain.services import user_service


class UserLoginTest(TestCase):
    def test_user_login(self):
        user = user_service.create_user(username='test1', password='test2')

        response = self.client.post(
            '/api/users/login/',
            data={
                'username': 'test1',
                'password': 'test2'
            }
        )
        assert response.status_code == 200
        result = response.json()
        assert result['id'] == user.id
        assert result['username'] == 'test1'
        assert result['access_token']
        assert 'password' not in result

    def test_user_login_validation(self):
        user = user_service.create_user(username='test1', password='test2')

        response = self.client.post(
            '/api/users/login/',
            data={
                'username': 'test1',
                'password': 'wrong'  # 패스워드 틀린경우
            }
        )
        assert response.status_code == 400
        result = response.json()
        assert result['detail'] == '패스워드가 일치하지 않습니다.'

    def test_user_login_validation2(self):
        user_service.create_user(username='test1', password='test2')

        response = self.client.post(
            '/api/users/login/',
            data={
                'username': 'wrong',  # 존재하지 않는 username
                'password': 'test2'
            }
        )
        assert response.status_code == 404

    def test_user_login_validation3(self):
        response = self.client.post(
            '/api/users/login/',
            data={
                'username': '',  # username 미입력
                'password': 'test2'
            }
        )
        assert response.status_code == 400
        result = response.json()
        assert result['detail'] == 'username 은 필수 입력값 입니다.'

    def test_user_login_validation4(self):
        response = self.client.post(
            '/api/users/login/',
            data={
                'username': 'username',
                'password': ''  # password 미입력
            }
        )
        assert response.status_code == 400
        result = response.json()
        assert result['detail'] == 'password 은 필수 입력값 입니다.'
