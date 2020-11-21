from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.domain.entities import User


class UserJoinView(APIView):
    user_service_factory = None

    def post(self, request, *args, **kwargs):
        user_service = self.user_service_factory.get()
        user = user_service.create_user(
            username=request.data.get('username', None),
            password=request.data.get('password', None)
        )
        user_entity = User.convert_repo_model_to_entity(user)
        return Response(user_entity.to_dict(), status=status.HTTP_201_CREATED)
