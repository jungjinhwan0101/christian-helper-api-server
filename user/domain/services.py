from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions

from user.domain.repositories import UserDataBaseRepository
from user.token import AccessToken


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

    def get_user_by_access_token(self, access_token):
        if not access_token:
            return None
        token_payload = AccessToken.decrypt(access_token)
        try:
            user = self.find_by_id(token_payload['id'])
        except ObjectDoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid Token.'))
        is_valid = token_payload == user.access_token.payload
        return user if is_valid else None


user_service = UserService(db_repo=UserDataBaseRepository)
