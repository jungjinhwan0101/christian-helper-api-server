from rest_framework import status
from rest_framework.response import Response
from api.views.base import BaseView
from user.usecases import UserJoinCommand


class UserJoinView(BaseView):
    def post(self, request, *args, **kwargs):
        _, user = UserJoinCommand().execute(data=request.data)
        data = {'id': user.id, 'username': user.username}
        return Response(data, status=status.HTTP_201_CREATED)
