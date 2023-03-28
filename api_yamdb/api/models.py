from django.db import models


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
    # Делать валидацию только для годов от Р.Х.?
    year = models.IntegerField(
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
        related_name='titles',
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

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year',)

    def __str__(self):
        return self.name
