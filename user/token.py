import json
from cryptography.fernet import Fernet
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions

from user.domain.services import user_service


class AccessToken:
    @classmethod
    def _encrypt_access_token(cls, data):
        cipher = Fernet(settings.USER_ACCESS_TOKEN_SECRET_KEY)
        token_payload = json.dumps(data).encode()
        return cipher.encrypt(token_payload).decode()

    @classmethod
    def _get_token_payload(cls, repo_user):
        return {
            'id': repo_user.id,
            'username': repo_user.username
        }

    @classmethod
    def decrypt_access_token(cls, access_token):
        cipher = Fernet(settings.USER_ACCESS_TOKEN_SECRET_KEY)
        token_payload = cipher.decrypt(access_token.encode()).decode()
        return json.loads(token_payload)

    @classmethod
    def obtain_access_token(cls, repo_user):
        return AccessToken._encrypt_access_token(cls._get_token_payload(repo_user))

    @classmethod
    def get_user_by_access_token(cls, access_token):
        if not access_token:
            return None
        token_payload = cls.decrypt_access_token(access_token)
        try:
            repo_user = user_service.find_by_id(token_payload['id'])
        except ObjectDoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid Token.'))
        is_valid = cls.decrypt_access_token(access_token) == cls._get_token_payload(repo_user)
        return repo_user if is_valid else None
