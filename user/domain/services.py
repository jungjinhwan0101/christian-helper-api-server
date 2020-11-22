from user.domain.repositories import UserDataBaseRepository


class UserService:
    def __init__(self, repository):
        self.repository = repository

    def create_user(self, username, password=None):
        repo_user = self.repository.create(username, password)
        return repo_user

    def find_by_id(self, user_id):
        repo_user = self.repository.find(filters={'id': user_id}).get()
        return repo_user

    def find_by_username(self, username):
        repo_user = self.repository.find(filters={'username': username}).get()
        return repo_user


user_service = UserService(UserDataBaseRepository)
