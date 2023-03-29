from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from reviews.models import Title
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Получить список отзывов на произведение"""
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
