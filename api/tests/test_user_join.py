from django.test import TestCase


class UserJoinTest(TestCase):
    def test_user_join(self):
        response = self.client.post(
            '/api/users/join/',
            data={
                'username': 'test1',
                'password': 'test2'
            }
        )
        assert response.status_code == 201
        result = response.json()
        assert result['id']
        assert result['username'] == 'test1'
        assert 'password' not in result

    def test_user_join_validation(self):
        response = self.client.post(
            '/api/users/join/',
            data={
                'username': '',  # 아이디가 공백인 경우
                'password': 'test2'
            }
        )
        assert response.status_code == 400
        result = response.json()
        assert result['detail'] == 'username 은 필수 입력값 입니다.'

    def test_user_join_validation2(self):
        response = self.client.post(
            '/api/users/join/',
            data={
                'username': 'test1',
                'password': ''  # 패스워드가 공백인 경우
            }
        )
        assert response.status_code == 400
        result = response.json()
        assert result['detail'] == 'password 은 필수 입력값 입니다.'
