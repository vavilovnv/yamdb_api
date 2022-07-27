from rest_framework import serializers

from users.models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'username',
        )


class CreateTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'confirmation_code',
        )
