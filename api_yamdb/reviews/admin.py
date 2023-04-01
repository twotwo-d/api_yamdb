from django.contrib import admin

from .models import Category, Comment, Genre, GenreToTitle, Title, Review

admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(GenreToTitle)
admin.site.register(Review)
admin.site.register(Comment)
