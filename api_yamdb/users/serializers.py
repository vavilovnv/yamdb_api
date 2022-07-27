from rest_framework import serializers

from .models import CustomUser


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'bio',
        )

