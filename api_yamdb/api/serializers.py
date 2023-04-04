import re

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""
    slug = serializers.SlugField(
        allow_blank=False,
        max_length=50,
        validators=[UniqueValidator(
            queryset=Genre.objects.all(),
            message='Такой идентификатор уже существует'
        )]
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""
    slug = serializers.SlugField(
        allow_blank=False,
        max_length=50,
        validators=[UniqueValidator(
            queryset=Category.objects.all(),
            message='Такой идентификатор уже существует'
        )]
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор заголовков"""
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
        required=True
    )
    category = serializers.SlugRelatedField(
        many=False,
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        return obj.calc_rating()


class TitleViewSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения заголовков"""
    genre = GenreSerializer(many=True, required=True)
    category = CategorySerializer(many=False, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category',
        )

    def get_rating(self, obj):
        return obj.calc_rating()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError(
                'Оценка должна быть в диапазоне от 1 до 10'
            )
        return value

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            author = request.user
            if (
                Review.objects.filter(title_id=title_id, author=author)
                .exists()
            ):
                raise serializers.ValidationError(
                    'Вы уже добавляли отзыв на это произведение'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Создадим сериалайзер для класса пользователь"""

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        ]


class CreateUserSerializer(serializers.Serializer):
    """Создадим сериалайзер для регистрации пользователей"""

    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.RegexField(
        required=True,
        max_length=150,
        regex=r'^[\w.@+-]+\Z',
    )

    # class Meta:
    #    validators = [
    #        UniqueTogetherValidator(
    #            queryset=User.objects.all(),
    #            fields=['username', 'email'],
    #        )
    #    ]

    def validate_username(self, value):
        """Проверим указанное имя пользователя"""

        if value.lower() == 'me':
            raise serializers.ValidationError(
                {'Выберете другое имя пользователя'})
        return value

    def validate_regex_in_username(self, value):
        """Проверим username на недопустимые символы"""

        regex = r'^[\w.@+-]+\Z'
        if not re.match(regex, value.username):
            raise serializers.ValidationError(
                {'Используются недопустимые символы: ^[\w.@+-]+\Z '}
            )
        return value

    def validate(self, data):
        """Проверим, существует ли пользователь с таким же email"""

        username = data.get('username')
        email = data.get('email')
        if (
            User.objects.filter(username=username).exists()
            and User.objects.get(username=username).email != email
        ):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if (
            User.objects.filter(email=email).exists()
            and User.objects.get(email=email).username != username
        ):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data


class AccessTokenSerializer(serializers.Serializer):
    """Создадим сериалайзер для получения JWT-токена"""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):  # def validate_confirmation_code(self, data):
        """Проверим код подтверждения"""

        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(user,
                                                   data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': 'Ошибка при вводе кода подтверждения'})
        return data
