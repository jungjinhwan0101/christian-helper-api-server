from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from rest_framework import exceptions
from user.token import AccessToken


class ORMUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def find_by_id(self, id):
        return self.get(id=id)

    def find_by_username(self, username):
        return self.get(username=username)

    def get_user_by_access_token(self, access_token):
        if not access_token:
            return None
        token_payload = AccessToken.decrypt(access_token)
        try:
            user = self.find_by_id(token_payload['id'])
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid Token.'))
        is_valid = token_payload == user.access_token.payload
        return user if is_valid else None