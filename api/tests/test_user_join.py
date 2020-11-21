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
