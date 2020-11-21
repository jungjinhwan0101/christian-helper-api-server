from user.domain.entities import User


class UserService:
    def __init__(self, repository):
        self.repository = repository

    def create_user(self, username, password):
        repo_user = self.repository.create(username, password)
        return User.convert_repo_model_to_entity(repo_user)
