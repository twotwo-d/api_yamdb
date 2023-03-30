from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .permissions import (IsAdminModeratorAuthorOrReadOnly,
                          IsAdminUserOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


class CreateDeleteListViewSet(mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateDeleteListViewSet):
    """Получить список категорий произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminUserOrReadOnly,)


class GenreViewSet(CreateDeleteListViewSet):
    """Получить список жанров произведений"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminUserOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Получить список произведений"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    """Получить список отзывов на произведение"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Получить список комментариев к отзыву"""
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
