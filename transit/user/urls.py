from django.urls import path
from .views import UserViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

user_list = UserViewSet.as_view({"get": "list"})
user_create = UserViewSet.as_view({"post": "create"})
user_detail = UserViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register", user_create, name="user-register"),
    path("<str:pk>/", user_detail, name="user-detail"),
]
