from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.views.base import BaseView
from user.domain.services import user_service


class UserDetailPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return view.kwargs['pk'] == request.user.id
        return False

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


class UserDetailView(BaseView):
    user_service_factory = None
    permission_classes = [UserDetailPermission, ]

    def get(self, request, pk, *args, **kwargs):
        user = user_service.find_by_id(pk)
        self.check_object_permissions(self.request, user)
        data = {'id': user.id, 'username': user.username}
        return Response(data, status=status.HTTP_200_OK)
