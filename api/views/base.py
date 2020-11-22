from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.exceptions import ValidationError


class BaseView(APIView):
    def handle_exception(self, exc):
        try:
            return super().handle_exception(exc)
        except ValidationError as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
