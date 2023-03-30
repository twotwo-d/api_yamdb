from api.permissions import IsAdminUser
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (AccessTokenSerializer, CreatUserSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """Создадим модель пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'username'
    seach_fields = ['username']
    http_method_names = ['post', 'patch', 'get', 'delete',]

    @action(
            methods=['patch', 'get'],
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


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Создадим функцию для регистрации пользователей"""

    serializer = CreatUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    if (
        User.objects.filter(email=email).exists()
        or User.objects.filter(username=username).exists()
    ):
        raise ValidationError(
            'Пользователь с таким e-mail или username уже существует'
        )
    user, code_created = User.objects.get_or_create(
        email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
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
