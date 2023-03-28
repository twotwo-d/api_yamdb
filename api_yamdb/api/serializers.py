from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""
    slug = serializers.CharField(
        allow_blank=False,
        validators=[UniqueValidator(
            max_length=50,
            queryset=Genre.objects.all(),
            message='Такой идентификатор уже существует'
        )]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""
    slug = serializers.CharField(
        allow_blank=False,
        validators=[UniqueValidator(
            max_length=50,
            queryset=Category.objects.all(),
            message='Такой идентификатор уже существует'
        )]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор заголовков"""
    genre = GenreSerializer(many=True, required=True,)
    category = CategorySerializer(many=False, required=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category',
        )
