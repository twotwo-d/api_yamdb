from api.permissions import IsAdminUser
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (AccessTokenSerializer, CreateUserSerializer,
                          UserSerializer)


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
    user_exists = (
        User.objects.filter(email=email).exists()
        or User.objects.filter(username=username).exists()
    )
    if user_exists:
        if (
            User.objects.filter(email=email).exists()
            and not User.objects.filter(username=username).exists()
        ):
            return Response(
                {'message': 'Пользователь с таким email уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif (
            not User.objects.filter(email=email).exists()
            and User.objects.filter(username=username).exists()
        ):
            return Response(
                {'message': 'Пользователь с таким username уже существует'},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'message': 'Пользователь уже зарегистрирован'},
                status=status.HTTP_200_OK
            )
    user, code_created = User.objects.get_or_create(
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
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    try:
        user = User.objects.get(
            username=username,
            confirmation_code=confirmation_code,
        )
    except User.DoesNotExist:
        return Response(
            {'message': 'Ваш токен не прошёл проверку'},
            status=status.HTTP_400_BAD_REQUEST
        )
    user.confirmation_code = ''
    user.save()
    try:
        jwt_token = RefreshToken.for_user(user)
    except TokenError as e:
        return Response(
            {'message': f'Ошибка при создании токена: {e}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response(
        {'token': f'{jwt_token.access_token}'},
        status=status.HTTP_200_OK
    )
