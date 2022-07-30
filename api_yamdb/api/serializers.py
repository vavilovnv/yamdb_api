from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import ValidationError

from reviews.models import Category, Genre, Title


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
        slug_field='category',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate(self, value):
        """Проверка присвоения категории"""
        if Title.objects.filter(category=value['category']).exists():
            raise ValidationError('Произведению уже присвоена категория')
        return value
