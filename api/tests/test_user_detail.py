from django.test import TestCase
from user.models import ORMUser


class UserJoinTest(TestCase):
    def setUp(self):
        repo_user = ORMUser.objects.create_user(username='test1')
        self.user_id = repo_user.id
        self.auth_token_header = {
            'X-HTTP-ACCESS-TOKEN': repo_user.access_token.obtain_token()
        }

    def test_user_get(self):
        user_id = self.user_id
        auth_token_header = self.auth_token_header

        response = self.client.get(
            f'/api/users/{user_id}/',
            **auth_token_header
        )
        assert response.status_code == 200

        result = response.json()
        assert result['id'] == user_id
        assert result['username'] == 'test1'

    def test_user_get_2(self):
        user_id = self.user_id
        auth_token_header = self.auth_token_header

        assert user_id != 2
        response = self.client.get(f'/api/users/2/', **auth_token_header)

        assert response.status_code == 403

    def test_user_get_validation(self):
        response = self.client.get(f'/api/users/wrong/')
        assert response.status_code == 404

    def test_user_get_validation2(self):
        response = self.client.get(f'/api/users/-1/')
        assert response.status_code == 404
