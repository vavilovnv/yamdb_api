from django.contrib.auth import get_user_model
from django.db.models import Avg
import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import ValidationError

from reviews.models import Comment, Review, Category, Genre, Title, GenreTitle

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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class ReadTitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        if isinstance(rating, int):
            return round(rating)
        return rating


class CreateTitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title

    def validate(self, value):
        """Проверяем присвоена ли категория произведению"""
        if Title.objects.filter(category=value['category']).exists():
            raise ValidationError('Произведению уже присвоена категория')
        return value

    def validate_year(self, value):
        """Год выпуска произведения не может быть больше текущего"""
        current_year = dt.datetime.now().year
        if current_year > value.year:
            raise ValidationError(
                'Год выпуска произведения не может быть больше текущего'
            )
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
