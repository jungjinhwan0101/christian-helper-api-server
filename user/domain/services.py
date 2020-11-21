class UserService:
    def __init__(self, repository):
        self.repository = repository

    def create_user(self, username, password=None):
        repo_user = self.repository.create(username, password)
        return repo_user

    def find_by_id(self, user_id):
        repo_user = self.repository.find_by_id(user_id)
        return repo_user
