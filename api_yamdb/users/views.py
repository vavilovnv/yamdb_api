from rest_framework import viewsets

from users.models import CustomUser
from .serializers import UsersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
