from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Subscription, User
from users.validators import unique_user_subscribe_validate


class ShortRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор сокращенного отображения рецепта пользователя. """

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class CustomUserCreateSerializer(UserCreateSerializer):
    """ Сериализатор создания объекта пользователя. Переопределяет модель
    и поля сериализации для djoser'a."""

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        ]


class CustomUserSerializer(UserSerializer):
    """ Сериализатор модели пользователя. """

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Мета класс модели пользователя. Переопределяет модель
        и поля сериализации для djoser'a."""

        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]

    def get_is_subscribed(self, user):
        """Метод определения существования подписки на пользователя."""
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user,
            author=user
        ).exists()


class FullVievUserSerializer(CustomUserSerializer):
    """Модель сериализатора для репрезентации USER'a
    с полным прпедставлением, включая рецепты."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        """Мета класс наследованный от кастомногог сериализатора модели
        пользователя. Добавляет инфформацию о рецептах к стандартным полям."""

        model = CustomUserSerializer.Meta.model
        fields = CustomUserSerializer.Meta.fields + ['recipes',
                                                     'recipes_count']

    def get_recipes(self, user):
        request = self.context.get('request')
        recipes = Recipe.objects.filter(author=user)

        if not request or request.user.is_anonymous:
            return False

        limit = request.query_params.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        return ShortRecipeSerializer(
            recipes,
            many=True,
            context={'request': request}
        ).data

    def get_recipes_count(self, user):
        """Метод выборки количества рецептов пользователя."""
        return user.recipe.all().count()


class UserSubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор подписки на автора"""

    class Meta:
        """Поля модели подписки."""

        model = Subscription
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author'),
                message='Вы уже подписаны на этого автора.'
            )
        ]
        validators = unique_user_subscribe_validate

    def to_representation(self, instance):
        """Репрезентация подписки в виде модели пользователя."""

        return CustomUserSerializer(
            instance.author,
            context={'request': self.context.get('request')}
        ).data


class SubscriptionsSerializer(UserSubscribeSerializer):
    """Сериализатор всех подписок текущего пользователя."""

    class Meta:
        """Поля модели подписки"""
        model = Subscription
        fields = ('user', 'author')

    def to_representation(self, instance):
        """Метод репрезентации подписок.
        Возвращает пользователя с рецептами."""

        return FullVievUserSerializer(
            instance.author,
            context={'request': self.context.get('request')}
        ).data
