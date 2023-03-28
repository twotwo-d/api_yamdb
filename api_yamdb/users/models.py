from django.db import models
from django.contrib.auth.models import AbstractUser


ANONYM = 'anonym'
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
        (ANONYM, 'anonym'),
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
]


class User(AbstractUser):
    """Create the model User for adding new users
    and fixing useres roles"""

    username = models.TextField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=254,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    # role = models.CharField(
    #    verbose_name='роль пользователя',
    #    max_length=10,
    #    choices=ROLES,
    #    default='user',
    # )
    # confirmation_code = models.CharField(
    #    verbose_name='Код подтверждения',
    # )


class Meta:
    verbose_name_plural = 'Пользователи'
    verbose_name = 'Пользователь'

    def __str__(self):
        return self.username
