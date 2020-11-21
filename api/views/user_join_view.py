from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UserJoinView(APIView):
    user_service_factory = None

    def post(self, request, *args, **kwargs):
        user_service = self.user_service_factory.get()
        user = user_service.create_user(
            username=request.data.get('username', None),
            password=request.data.get('password', None)
        )
        data = {
            'id': user.id,
            'username': user.username
        }
        return Response(data, status=status.HTTP_201_CREATED)
