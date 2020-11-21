from django.test import TestCase
from user.models import ORMUser


class UserCreateTest(TestCase):
    def test_orm_user_create(self):
        repo_user = ORMUser.objects.create_user(username='test1', password='test2')
        assert repo_user.username == 'test1'
        assert repo_user.check_password('test2') is True
        assert repo_user.check_password('test3') is False

