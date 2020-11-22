import json
from cryptography.fernet import Fernet
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from user.domain.factories import UserServiceFactory


def _encrypt_access_token(data):
    cipher = Fernet(settings.USER_ACCESS_TOKEN_SECRET_KEY)
    token_payload = json.dumps(data).encode()
    return cipher.encrypt(token_payload).decode()


def _get_token_payload(repo_user):
    return {
        'id': repo_user.id,
        'username': repo_user.username
    }


def decrypt_access_token(access_token):
    cipher = Fernet(settings.USER_ACCESS_TOKEN_SECRET_KEY)
    token_payload = cipher.decrypt(access_token.encode()).decode()
    return json.loads(token_payload)


def obtain_access_token(repo_user):
    return _encrypt_access_token(_get_token_payload(repo_user))


def get_user_by_access_token(access_token):
    if not access_token:
        return None
    token_payload = decrypt_access_token(access_token)
    user_service = UserServiceFactory.get()
    try:
        repo_user = user_service.find_by_id(token_payload['id'])
    except ObjectDoesNotExist:
        raise exceptions.AuthenticationFailed(_('Invalid Token.'))
    is_valid = decrypt_access_token(access_token) == _get_token_payload(repo_user)
    return repo_user if is_valid else None
