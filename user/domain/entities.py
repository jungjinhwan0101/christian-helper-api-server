class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @classmethod
    def convert_repo_model_to_entity(cls, repo_model):
        return cls(id=repo_model.id, username=repo_model.username)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def get_token_payload(self):
        return {
            'id': self.id,
            'username': self.username
        }
