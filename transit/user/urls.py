from django.urls import path
from .views import UserViewSet

user_list = UserViewSet.as_view({"get": "list", "post": "create"})
user_detail = UserViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("<str:pk>/", user_detail, name="user-detail"),
    path("", user_list, name="agency-user"),
]
