from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Создадим сериалайзер для класса пользователь"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'bio', 'email', 'role', ]


class CreateUserSerializer(serializers.Serializer):
    """Создадим сериалайзер для регистрации пользователей"""

    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.RegexField(
        required=True,
        max_length=150,
        regex=r'^[\w.@+-]+\Z',
    )

    def validate(self, data):
        """Проверим указанное имя пользователя"""

        if data['username'] == 'me':
            raise serializers.ValidationError(
                {'Выберете другое имя пользователя'})
        return data


class AccessTokenSerializer(serializers.Serializer):
    """Создадим сериалайзер для получения JWT-токена"""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        """Проверим код подтверждения"""

        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(user,
                                                   data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': 'Ошибка при вводе кода подтверждения'})
        return data
