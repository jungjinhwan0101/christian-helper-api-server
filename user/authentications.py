import json

from cryptography.fernet import Fernet
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from user.domain.entities import User
from user.domain.factories import UserServiceFactory


class AccessTokenAuthentication(BaseAuthentication):
    def get_authorization_header(self, request):
        return request.META.get('X-HTTP-ACCESS-TOKEN', None)

    def authenticate(self, request):
        access_token = self.get_authorization_header(request)
        if not access_token:
            return None

        cipher = Fernet(settings.USER_ACCESS_TOKEN_SECRET_KEY)
        decrypt_token_info = cipher.decrypt(access_token.encode()).decode()
        decrypt_token_info = json.loads(decrypt_token_info)

        user_service = UserServiceFactory.get()
        try:
            repo_user = user_service.find_by_id(decrypt_token_info['id'])
        except ObjectDoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid Access-token.'))

        user_entity = User.convert_repo_model_to_entity(repo_user)
        if user_entity.check_access_token(access_token, secret_key=settings.USER_ACCESS_TOKEN_SECRET_KEY):
            return (repo_user, None)
        else:
            return None
