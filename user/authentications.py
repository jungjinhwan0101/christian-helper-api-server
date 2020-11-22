from rest_framework.authentication import BaseAuthentication

from user.token import get_user_by_access_token


class AccessTokenAuthentication(BaseAuthentication):
    def get_authorization_header(self, request):
        return request.META.get('X-HTTP-ACCESS-TOKEN', None)

    def authenticate(self, request):
        access_token = self.get_authorization_header(request)
        user = get_user_by_access_token(access_token)
        return (user, None) if user else None
