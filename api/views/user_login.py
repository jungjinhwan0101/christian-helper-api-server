from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from api.exceptions import ValidationError
from api.views.base import BaseView
from user.token import obtain_access_token
from user.domain.entities import User


class UserLoginView(BaseView):
    user_service_factory = None

    def post(self, request, *args, **kwargs):
        username = self.get_data('username')
        password = self.get_data('password')

        user_service = self.user_service_factory.get()
        try:
            repo_user = user_service.find_by_username(username)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not repo_user.check_password(password):
            raise ValidationError('패스워드가 일치하지 않습니다.')

        user_entity = User.convert_repo_model_to_entity(repo_user)
        result = {}
        result.update(user_entity.to_dict())
        result.update({
            'access_token': obtain_access_token(repo_user)
        })
        return Response(result, status=status.HTTP_200_OK)
