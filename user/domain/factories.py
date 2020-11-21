from user.domain.repositories import UserDataBaseRepository
from user.domain.services import UserService


class UserRepositoryFactory:
    @staticmethod
    def get():
        return UserDataBaseRepository


class UserServiceFactory:
    @staticmethod
    def get():
        repository = UserRepositoryFactory.get()
        return UserService(repository)
