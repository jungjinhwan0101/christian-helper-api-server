from user.models import ORMUser


class UserDataBaseRepository:
    @classmethod
    def create(cls, username, password):
        return ORMUser.objects.create_user(username, password)

    @classmethod
    def find(cls, filters):
        return ORMUser.objects.filter(**filters)
