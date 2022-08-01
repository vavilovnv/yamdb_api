from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    # title = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    category = SlugRelatedField(
        slug_field='title',
        # было slug_field='category',
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='title',
        # было slug_field='genre',
        queryset=Category.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate(self, value):
        """Проверяем присвоена ли категория произведению"""
        if Title.objects.filter(category=value['category']).exists():
            raise ValidationError('Произведению уже присвоена категория')
        return value


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
