from api.permissions import IsAdminUser
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import (IsAdminModeratorAuthorOrReadOnly,
                          IsAdminUserOrReadOnly)
from .serializers import (AccessTokenSerializer, CategorySerializer,
                          CommentSerializer, CreateUserSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TitleViewSerializer, UserSerializer)


class CreateDeleteListViewSet(mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateDeleteListViewSet):
    """Получить список категорий произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class GenreViewSet(CreateDeleteListViewSet):
    """Получить список жанров произведений"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Получить список произведений"""
    queryset = Title.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleSerializer
        return TitleViewSerializer


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


class UserViewSet(viewsets.ModelViewSet):
    """Создадим модель пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'username'
    search_fields = ['username']
    filter_backends = [SearchFilter]
    http_method_names = ['post', 'patch', 'get', 'delete', ]
    pagination_class = LimitOffsetPagination

    @action(
        methods=['get', 'patch', ],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        """Создадим функцию для получения данных собственной учётной записи"""

        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(self.request.user,
                                    data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([AllowAny])
def signup(request):
    """Создадим функцию для регистрации пользователей"""

    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user, _ = User.objects.get_or_create(
        email=email,
        username=username
    )
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    send_mail(
        'Confirmation code',
        f'Ваш код подтверждения {confirmation_code}',
        settings.SENDING_EMAIL,
        [email],
        fail_silently=False
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    """Создадим функцию получения JWT-токена"""

    serializer = AccessTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        jwt_token = RefreshToken.for_user(request.user)
    except TokenError as e:
        return Response(
            {'message': f'Ошибка при создании токена: {e}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response(
        {'token': f'{jwt_token.access_token}'},
        status=status.HTTP_200_OK
    )
