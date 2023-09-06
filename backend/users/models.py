from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram_backend import model_settings as set


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        'Имя пользователя',
        max_length=set.USER_USERNAME_LENGTH,
        unique=True,
        null=False,
        blank=False,
        help_text='Здесь должен быть логин для входа')

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=set.USER_EMAIL_LENGTH,
        null=False,
        blank=False,
        unique=True,
        help_text='Введите Ваш email'
    )
    first_name = models.CharField(
        'Имя',
        max_length=set.USER_FIRST_NAME_LENGTH,
        null=False,
        blank=False,
        help_text='Например "Владимир"'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=set.USER_LAST_NAME_LENGTH,
        null=False,
        blank=False,
        help_text='Например "Петров"'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        """Мета настройки отображения модели."""

        ordering = ['first_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Строковое отображение модели пользователя."""

        return (f'{self.first_name} {self.last_name}')


class Subscription(models.Model):
    """Модель подписки на автора."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        """Сортировка выдачи подписок и проверка уникальности."""

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow',
            )
        ]
        ordering = ['-created_at']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        """Строковое отображение модели подписки на автора."""

        return f'{self.user} подписан на {self.author}.'
