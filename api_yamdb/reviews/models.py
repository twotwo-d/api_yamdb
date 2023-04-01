from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg

from users.models import User
from .validators import year_validator


class Genre(models.Model):
    '''Категории жанров'''
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр',
        help_text='Укажите жанр'
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Идентификатор',
        help_text='Укажите идентификатор жанра',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категории (типы) произведений"""
    name = models.CharField(
        max_length=256,
        verbose_name='Категория (тип) произведения',
        help_text='Укажите категорию (тип) произведения'
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Идентификатор',
        help_text='Укажите идентификатор категории (типа) произведения',
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения"""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
        help_text='Укажите название произведения'
    )
    year = models.IntegerField(
        validators=[year_validator],
        verbose_name='Год выхода',
        help_text='Укажите год выхода произведения'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Добавьте краткое описание произведения',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreToTitle',
        verbose_name='Жанр',
        help_text='Добавьте Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория',
        help_text='Добавьте категорию произведения'
    )

    def calc_rating(self):
        return self.reviews.aggregate(rating=Avg('score'))['rating']

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year',)

    def __str__(self):
        return self.name


class GenreToTitle(models.Model):
    """Связь произведения с жанром"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """Отзывы на произведения"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        max_length=150,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        validators=[
            MaxValueValidator(10, message='Оценка не может быть больше 10.'),
            MinValueValidator(1, message='Оценка не может быть меньше 1.'),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return f'{self.title} - {self.author}'


class Comment(models.Model):
    """Комментарии к отзывам"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        max_length=150,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.review} - {self.author}'
