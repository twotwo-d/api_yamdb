from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title


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

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class TitleViewSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения заголовков"""
    genre = GenreSerializer(many=True, required=True)
    category = CategorySerializer(many=False, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')

    def validate_score(self, value):
        if not 1 <= value <= 10:
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
