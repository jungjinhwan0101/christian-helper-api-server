from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from api.views.base import BaseView
from user.usecases import UserLoginCommand


class UserLoginView(BaseView):

    def post(self, request, *args, **kwargs):
        try:
            _, result = UserLoginCommand().execute(request.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = result['user']
        data = {
            'id': user.id,
            'username': user.username,
            'access_token': result['access_token']
        }
        return Response(data, status=status.HTTP_200_OK)
