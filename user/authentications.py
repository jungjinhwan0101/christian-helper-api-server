from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from base.token import decrypt_access_token
from user.domain.entities import User
from user.domain.factories import UserServiceFactory


class AccessTokenAuthentication(BaseAuthentication):
    def get_authorization_header(self, request):
        return request.META.get('X-HTTP-ACCESS-TOKEN', None)

    def authenticate(self, request):
        access_token = self.get_authorization_header(request)
        if not access_token:
            return None

        token_payload = decrypt_access_token(access_token)

        user_service = UserServiceFactory.get()
        try:
            repo_user = user_service.find_by_id(token_payload['id'])
        except ObjectDoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid Token.'))

        user_entity = User.convert_repo_model_to_entity(repo_user)

        if token_payload == user_entity.get_token_payload():
            return (repo_user, None)
        else:
            return None
