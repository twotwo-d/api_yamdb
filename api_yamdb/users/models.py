from django.contrib.auth.models import AbstractUser
from django.db import models

"""Согласно ТЗ опишем возможные роли пользователей"""

ANONYM = 'anonym'
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES = [
    (ANONYM, 'anonym'),
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
]


class User(AbstractUser):
    """Создали модель Пользователь и указали роли в ROLE_CHOICES"""

    email = models.EmailField(
        unique=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=100,
        choices=ROLE_CHOICES,
        default='user',
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=150,
        editable=False,
        null=True,
        blank=True,
        unique=False
    )

    @property
    def is_user(self):
        """Проверим наличие прав у пользователя"""
        return self.role == self.USER

    @property
    def is_admin(self):
        """Проверим наличие прав у администратора"""
        return any(
            [self.role == ADMIN, self.is_superuser, self.is_staff]
        )

    @property
    def is_moderator(self):
        """Проверим наличие прав у модератора"""
        return self.role == MODERATOR


class Meta:
    verbose_name_plural = 'Пользователи'
    verbose_name = 'Пользователь'
    ordering = ('username',)
    constraints = [
        models.UniqueConstraint(
            fields=['username', 'email'],
            name='unique_fields'
        )
    ]

    def __str__(self):
        return self.username
