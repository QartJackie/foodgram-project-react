from django.contrib import admin

from users.models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    """Регистрация модели пользователя в админке."""

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
    )
    list_filter = (
        'email',
        'first_name',
        'recipe__tags'
    )
    search_fields = ('email', 'first_name')
    empty_value_display = '-пусто-'


class SubscriptionAdmin(admin.ModelAdmin):
    """Регистрация модели подписки в админке."""

    list_display = (
        'id',
        'user',
        'author',
        'created_at',
    )
    list_filter = ('author__recipe__tags',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
