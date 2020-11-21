from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from api.views.base import BaseView
from user.domain.entities import User


class UserDetailView(BaseView):
    user_service_factory = None

    def get(self, request, pk, *args, **kwargs):
        user_service = self.user_service_factory.get()
        try:
            user = user_service.find_by_id(pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_entity = User.convert_repo_model_to_entity(user)
        return Response(user_entity.to_dict(), status=status.HTTP_200_OK)
