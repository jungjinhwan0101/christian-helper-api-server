from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.exceptions import RequireInputError


class BaseView(APIView):
    def get_data(self, request, field_name, require=True):
        value = request.data.get(field_name, None)
        if require and not value:
            raise RequireInputError(f'{field_name} 은 필수 입력값 입니다.')
        return value

    def handle_exception(self, exc):
        try:
            return super().handle_exception(exc)
        except RequireInputError as e1:
            return Response(data={'detail': str(e1)}, status=status.HTTP_400_BAD_REQUEST)