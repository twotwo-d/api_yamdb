from django.contrib import admin

from .models import Category, Comment, Genre, GenreToTitle, Review, Title


class GenreToTitleInline(admin.TabularInline):
    model = GenreToTitle
    extra = 1


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = [GenreToTitleInline]


admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
