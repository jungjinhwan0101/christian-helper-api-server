from user.domain.repositories import UserDataBaseRepository


class UserService:
    def __init__(self, db_repo):
        self.db_repo = db_repo

    def create_user(self, username, password=None):
        repo_user = self.db_repo.create(username, password)
        return repo_user

    def find_by_id(self, user_id):
        repo_user = self.db_repo.find(filters={'id': user_id}).get()
        return repo_user

    def find_by_username(self, username):
        repo_user = self.db_repo.find(filters={'username': username}).get()
        return repo_user


user_service = UserService(db_repo=UserDataBaseRepository)
