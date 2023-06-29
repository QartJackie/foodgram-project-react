import base64
import webcolors
from djoser.serializers import UserSerializer, UserCreateSerializer
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator

from api.utils import convert_ingredient_data_for_create
from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredientsAmount, ShoppingCart, Tag)
from users.models import User, Subscription


class Hex2NameColor(serializers.Field):
    """Модель сериализатора цветов, преобразующий
    hex-код цвета в строковое название."""

    def to_representation(self, value):
        """Функция репрезентации представления."""
        return value

    def to_internal_value(self, data):
        """Функция преобразования hex кода цвета в название-строку."""
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class Base64ImageField(serializers.ImageField):
    """Модель сериализатора изображений.
    Преобразует код base64 в изображение."""

    def to_internal_value(self, data):
        """Функция декодировки base64 в изображение."""

        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


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
        return False if request else Subscription.objects.filter(
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


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    color = Hex2NameColor()

    class Meta:
        """Представление полей тега."""
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов."""

    class Meta:
        """Представление полей ингредиента."""
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class ReadIngredientamountSerializer(serializers.ModelSerializer):
    """Вспомогательная модель сериализации ингредиентов модели для чтения.
    Дополняется количеством необходимого ингредиента."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredientsAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CreateIngredientamountSerializer(ReadIngredientamountSerializer):
    """Вспомогательная модель привязки ингридиента при создании рецепта."""

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredientsAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор создания и обновления рецептов."""

    tags = TagSerializer(read_only=True, many=True)
    author = serializers.StringRelatedField()
    ingredients = CreateIngredientamountSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=[MinValueValidator(
            limit_value=1,
            message='Время приготовления не может быть меньше 1 минуты.'
        )
        ]
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate(self, recipe_data):
        ingredients = self.initial_data.get('ingredients')
        if len(ingredients) <= 0:
            raise serializers.ValidationError(
                {'message': 'Добавьте ингредиенты'}
            )

        for ingredient in ingredients:
            amount = int(ingredient['amount'])
            if not amount > 0:
                raise serializers.ValidationError(
                    {'message':
                     'Нельзя установить количество '
                     f'ингредиента, равное {amount}'}
                )
        return recipe_data

    def create_ingredient_amount(self, ingredients, recipe):
        """Метод привязки ингридинета к рецепту."""

        ingredient_list = convert_ingredient_data_for_create(
            self, ingredients, recipe
        )
        RecipeIngredientsAmount.objects.bulk_create(
            [RecipeIngredientsAmount(
                **ingredient
            ) for ingredient in ingredient_list]
        )

    def create(self, validated_data):
        """Метод создания рецепта."""

        request = self.context.get('request')
        if not request.user and request.user.is_authenticated:
            return Response(
                {'message': 'Авторизуйтесь, чтобы добавить рецепт'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        tags = self.initial_data.get('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredient_amount(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Метод обновления рецепта."""

        request = self.context.get('request')
        recipe = get_object_or_404(Recipe, pk=instance.id)

        if not request.user and (
            request.user.is_authenticated
            and request.user == recipe.author
        ):
            return Response(
                {'message':
                 'Чтобы редактировать рецепт, нужно быть его автором.'},
                status=status.HTTP_403_FORBIDDEN
            )
        RecipeIngredientsAmount.objects.filter(recipe=instance).delete()
        tags = self.initial_data.get('tags')
        recipe.tags.set(tags)
        ingredients = validated_data.pop('ingredients')
        self.create_ingredient_amount(ingredients, instance)
        if validated_data.get('image'):
            instance.image = validated_data.pop('image')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        return instance

    def to_representation(self, instance):
        """Метод репрезентации сериализации через
        сериализатор для чтения рецептов."""

        return ReadRecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class ReadRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения рецептов."""

    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        """Метод получения ингридиента для чтения."""
        ingredients = RecipeIngredientsAmount.objects.filter(recipe=obj)
        return ReadIngredientamountSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        """Метод получения статуса избранного рецепта."""

        request = self.context.get('request')
        return False if not request else FavoriteRecipe.objects.filter(
            user_id=request.user.pk,
            recipe_id=obj.pk
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        """Метод получения статуса добавления рецепта в список покупок."""

        request = self.context.get('request')
        return False if not request else ShoppingCart.objects.filter(
            user_id=request.user.pk,
            recipe_id=obj.pk
        ).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор сокращенного отображения рецепта пользователя. """

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок."""

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'recipe',
            'user',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('recipe', 'user'),
                message='Вы уже добавили рецепт в список покупок.'
            )
        ]

    def to_representation(self, instance):
        """Метод репрезентации списка покупок в виде
        списка рецептов с кратким представлением."""

        request = self.context.get('request')
        return ShortRecipeSerializer(
            instance.recipe,
            context={'request': request}
        ).data


class FavoriteRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор избранных рецептов."""

    class Meta:
        model = FavoriteRecipe
        fields = (
            'id',
            'recipe',
            'user',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteRecipe.objects.all(),
                fields=('recipe', 'user'),
                message='Рецепт уже добавлен в избранное.'
            )
        ]

    def to_representation(self, instance):
        """Метод репрезентации списка покупок в виде
        списка рецептов с кратким представлением."""

        return ShortRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
