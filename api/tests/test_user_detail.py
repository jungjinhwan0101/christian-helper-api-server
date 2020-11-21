from django.test import TestCase

from user.domain.factories import UserServiceFactory


class UserJoinTest(TestCase):
    def test_user_get(self):
        user_service = UserServiceFactory.get()
        user = user_service.create_user(username='test1')
        user_id = user.id

        response = self.client.get(f'/api/users/{user_id}/')
        assert response.status_code == 200

        result = response.json()
        assert result['id'] == user_id
        assert result['username'] == 'test1'

    def test_user_get_2(self):
        response = self.client.get(f'/api/users/2/')
        assert response.status_code == 400
        result = response.json()
        assert result['detail'] == '유저가 존재하지 않습니다.'
