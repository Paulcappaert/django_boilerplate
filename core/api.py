from rest_framework import viewsets, status

from .serializers import UserSerializer
from .models import User
from .permissions import UserPermission


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserPermission]
