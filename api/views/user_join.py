from rest_framework import status
from rest_framework.response import Response
from api.views.base import BaseView
from user.domain.entities import User
from user.domain.services import user_service


class UserJoinView(BaseView):

    def post(self, request, *args, **kwargs):
        username = self.get_data('username')
        password = self.get_data('password')

        user = user_service.create_user(username=username, password=password)
        user_entity = User.convert_repo_model_to_entity(user)
        return Response(user_entity.to_dict(), status=status.HTTP_201_CREATED)
