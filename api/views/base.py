from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.exceptions import ValidationError


class BaseView(APIView):
    def get_data(self, field_name, require=True):
        value = self.request.data.get(field_name, None)
        if require and not value:
            raise ValidationError(f'{field_name} 은 필수 입력값 입니다.')
        return value

    def handle_exception(self, exc):
        try:
            return super().handle_exception(exc)
        except ValidationError as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
