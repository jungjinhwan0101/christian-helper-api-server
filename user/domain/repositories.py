from user.models import ORMUser


class UserDataBaseRepository:
    @classmethod
    def create(cls, username, password):
        return ORMUser.objects.create_user(username, password)

    @classmethod
    def find_by_id(cls, user_id):
        return ORMUser.objects.get(id=user_id)
