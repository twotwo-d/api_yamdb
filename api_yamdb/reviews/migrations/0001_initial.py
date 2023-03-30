# Generated by Django 3.2 on 2023-03-29 22:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите категорию (тип) произведения', max_length=256, verbose_name='Категория (тип) произведения')),
                ('slug', models.SlugField(help_text='Укажите идентификатор категории (типа) произведения', unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите жанр', max_length=256, verbose_name='Жанр')),
                ('slug', models.SlugField(help_text='Укажите идентификатор жанра', unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=150, verbose_name='Текст отзыва')),
                ('score', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10, message='Оценка не может быть больше 10.'), django.core.validators.MinValueValidator(1, message='Оценка не может быть меньше 1.')], verbose_name='Оценка произведения')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите название произведения', max_length=256, verbose_name='Название произведения')),
                ('year', models.IntegerField(help_text='Укажите год выхода произведения', verbose_name='Год выхода')),
                ('description', models.TextField(blank=True, help_text='Добавьте краткое описание произведения', verbose_name='Описание')),
                ('category', models.ForeignKey(blank=True, help_text='Добавьте категорию произведения', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(help_text='Добавьте Жанр произведения', related_name='titles', to='reviews.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ('-year',),
            },
        ),
    ]
