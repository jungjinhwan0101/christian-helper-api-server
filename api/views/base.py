from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.exceptions import ValidationError


class BaseView(GenericAPIView):
    def handle_exception(self, exc):
        try:
            return super().handle_exception(exc)
        except ValidationError as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
