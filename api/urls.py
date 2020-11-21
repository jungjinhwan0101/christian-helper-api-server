from django.urls import path
from api import views
from user.domain.factories import UserServiceFactory

urlpatterns = [
    path('users/<int:pk>/', views.UserDetailView.as_view(user_service_factory=UserServiceFactory)),
    path('users/join/', views.UserJoinView.as_view(user_service_factory=UserServiceFactory)),
    path('users/login/', views.UserLoginView.as_view(user_service_factory=UserServiceFactory))
]
