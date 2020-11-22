from django.urls import path
from api import views

urlpatterns = [
    path('users/<int:pk>/', views.UserDetailView.as_view()),
    path('users/join/', views.UserJoinView.as_view()),
    path('users/login/', views.UserLoginView.as_view())
]
