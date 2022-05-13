from .serializers import UserSerializer
from .models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post"]
    serializer_class = UserSerializer
    queryset = User.objects.all()
