from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from api.exceptions import ValidationError
from api.views.base import BaseView
from user.domain.entities import User


class UserDetailView(BaseView):
    user_service_factory = None

    def get(self, request, pk, *args, **kwargs):
        user_service = self.user_service_factory.get()
        try:
            user = user_service.find_by_id(pk)
        except ObjectDoesNotExist:
            raise ValidationError('유저가 존재하지 않습니다.')

        user_entity = User.convert_repo_model_to_entity(user)
        return Response(user_entity.to_dict(), status=status.HTTP_200_OK)
