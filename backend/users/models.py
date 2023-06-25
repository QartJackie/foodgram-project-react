from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        null=False,
        blank=False,
        help_text='Здесь должен быть логин для входа')

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        null=False,
        blank=False,
        unique=True,
        help_text='Введите Ваш email'
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        null=False,
        blank=False,
        help_text='Например "Владимир"'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        null=False,
        blank=False,
        help_text='Например "Петров"'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return (f'{self.first_name} {self.last_name}')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


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

    def __str__(self):
        return f'{self.user} подписан на {self.author}.'

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
