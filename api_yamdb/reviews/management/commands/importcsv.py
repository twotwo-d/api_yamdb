from django.core.management.base import BaseCommand

import pandas as pd

from reviews.models import (Category, Comment, Genre, GenreToTitle, Review,
                            Title, User,)


class Command(BaseCommand):
    """Команда для загрузки csv файлов в базу данных:
     python manage.py importcsv """

    help = 'Import to db from .csv files'

    def dbup_user(self):
        df = pd.read_csv('static/data/users.csv', sep=',')
        row_iter = df.iterrows()
        objs = [
            User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            for index, row in row_iter
        ]
        User.objects.bulk_create(objs)

    def dbup_genre(self):
        df = pd.read_csv('static/data/genre.csv', sep=',')
        row_iter = df.iterrows()
        objs = [
            Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            for index, row in row_iter
        ]
        Genre.objects.bulk_create(objs)

    def dbup_category(self):
        df = pd.read_csv('static/data/category.csv', sep=',')
        row_iter = df.iterrows()
        objs = [
            Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            for index, row in row_iter
        ]
        Category.objects.bulk_create(objs)

    def dbup_title(self):
        df = pd.read_csv('static/data/titles.csv', sep=',')
        row_iter = df.iterrows()
        objs = [
            Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(pk=row['category']),
            )
            for index, row in row_iter
        ]
        Title.objects.bulk_create(objs)

    def dbup_genretotitle(self):
        df = pd.read_csv('static/data/genre_title.csv', sep=',')
        row_iter = df.iterrows()
        objs = [
            GenreToTitle(
                id=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                genre=Genre.objects.get(pk=row['genre_id']),
            )
            for index, row in row_iter
        ]
        GenreToTitle.objects.bulk_create(objs)

    def dbup_review(self):
        df = pd.read_csv('static/data/review.csv', sep=',')
        row_iter = df.iterrows()
        objs = [
            Review(
                id=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                text=row['text'],
                author=User.objects.get(pk=row['author']),
                score=row['score'],
                pub_date=row['pub_date'],
            )
            for index, row in row_iter
        ]
        Review.objects.bulk_create(objs)

    def dbup_comment(self):
        df = pd.read_csv('static/data/comments.csv', sep=',')
        row_iter = df.iterrows()
        objs = [
            Comment(
                id=row['id'],
                review=Review.objects.get(pk=row['review_id']),
                text=row['text'],
                author=User.objects.get(pk=row['author']),
                pub_date=row['pub_date'],
            )
            for index, row in row_iter
        ]
        Comment.objects.bulk_create(objs)

    def handle(self, *args, **options):
        self.dbup_user()
        self.dbup_genre()
        self.dbup_category()
        self.dbup_title()
        self.dbup_genretotitle()
        self.dbup_review()
        self.dbup_comment()
