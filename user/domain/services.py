class UserService:
    def __init__(self, repository):
        self.repository = repository

    def create_user(self, username, password):
        repo_user = self.repository.create(username, password)
        return repo_user
