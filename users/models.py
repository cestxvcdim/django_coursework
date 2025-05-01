from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone_number = models.CharField(max_length=20, unique=True, **NULLABLE, verbose_name='номер телефона')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='фото профиля')
    country = models.CharField(max_length=50, **NULLABLE, verbose_name='страна')

    token = models.CharField(max_length=100, **NULLABLE, verbose_name='токен')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        permissions = [
            ('can_block_user', 'Can block user'),
        ]
