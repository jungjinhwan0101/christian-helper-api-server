from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from api.exceptions import ValidationError
from api.views.base import BaseView
from user.domain.services import user_service
from user.token import UserAccessToken


class UserLoginView(BaseView):

    def post(self, request, *args, **kwargs):
        username = self.get_data('username')
        password = self.get_data('password')

        try:
            user = user_service.find_by_username(username)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            raise ValidationError('패스워드가 일치하지 않습니다.')

        data = {
            'id': user.id,
            'username': user.username,
            'access_token': UserAccessToken.obtain_access_token(user)
        }
        return Response(data, status=status.HTTP_200_OK)
