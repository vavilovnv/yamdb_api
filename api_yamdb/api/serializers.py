from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review, Title

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели CustomUser."""

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'bio',
        )


class UserSerializerReadOnly(serializers.ModelSerializer):
    """Сериализатор модели CustomUser (чтение)."""

    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'bio',
        )


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор полей пользователя при регистрации."""

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                ('Нельзя использовать логин "me".'
                 'Пожалуйста, придумайте иное имя пользователя.')
            )
        return value


class CreateTokenSerializer(serializers.Serializer):
    """Сериализатор полей пользователя при получении access-токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
