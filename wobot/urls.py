from django.urls import path
from .views import UserAPIView, TaskAPIView, login
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("user", UserAPIView.as_view(), name="user_api"),
    path("task", TaskAPIView.as_view(), name="task_api"),
    path("auth", login, name="login_api"),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh_api")
]