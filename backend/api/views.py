from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingCart,
                            Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter, TagFilter
from api.pagination import LimitOffsetPagination
from api.permission import IsAuthorOrAdminOrReadOnly, IsAdminOrReadOnly
from api.serializers import (CreateRecipeSerializer, CustomUserSerializer,
                             FavoriteRecipesSerializer, IngredientSerializer,
                             ReadRecipeSerializer, ShoppingCartSerializer,
                             SubscriptionsSerializer, TagSerializer,
                             UserSubscribeSerializer)
from api.utils import get_shopping_list_file
from users.models import Subscription, User


class TagsViewSet(viewsets.ModelViewSet):
    """Вьюсет тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [IsAdminOrReadOnly, ]
    filter_backends = [TagFilter, ]
    search_fields = ['^name', ]
    pagination_class = None


class IngridientsViewSet(viewsets.ModelViewSet):
    """Вьюсет ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [IngredientFilter, ]
    search_fields = ['^name', ]
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов."""

    queryset = Recipe.objects.all()
    serializer_class = CreateRecipeSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Функция выбора сериализатора рецептов
        в зависимости от метода http."""

        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return CreateRecipeSerializer
        return ReadRecipeSerializer

    def perform_create(self, serializer):
        """Метод создания рецепта."""

        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Метод обновления рецепта."""

        serializer.save(author=self.request.user)

    @action(methods=['post', 'delete'], detail=True,
            url_name='favorite', url_path='favorite',
            permission_classes=(IsAuthenticated, ))
    def is_favorited_manage(self, request, pk):
        """Метод добавления рецепта или его удаления из избранного."""

        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = FavoriteRecipesSerializer(
                data={'user': request.user.pk, 'recipe': recipe.pk},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        favorited_recipe = get_object_or_404(
            FavoriteRecipe,
            user=request.user,
            recipe=recipe
        )
        favorited_recipe.delete()
        response_data = {'message': 'Рецепт удален из избранного.'}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True,
            url_name='shopping_cart', url_path='shopping_cart',
            permission_classes=(IsAuthenticated, ))
    def shopping_cart_manage(self, request, pk):
        """Менеджер списка покупок. Дообавляет или удаляет рецепт из списка."""

        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(
                data={'user': request.user.pk, 'recipe': recipe.pk},
                context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        cart = get_object_or_404(
            ShoppingCart,
            user=request.user,
            recipe=recipe
        )
        cart.delete()
        response_data = {
            'message': 'Теперь этот рецепт не в списке покупок'
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'],
            detail=False,
            url_name='download_shopping_cart',
            url_path='download_shopping_cart',
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Функция выгрузки списка покупок ингредиентов."""

        shopping_list_response = get_shopping_list_file(request)
        if shopping_list_response:
            return shopping_list_response
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllUserViewSet(UserViewSet):
    """Вьюсет пользователей."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=True,
            methods=['post', 'delete'],
            url_name='subscribe',
            url_path='subscribe',)
    def subscribe(self, request, id):
        """Метод подписки модели пользователя."""
        print('начало подписка')
        author = get_object_or_404(User, pk=id)
        data = {'user': request.user.pk, 'author': id}
        print(f'Перед тем как проверить метож {request.method}')
        if request.method == 'POST':
            serializer = UserSubscribeSerializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, author=author)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        subscription = get_object_or_404(
            Subscription,
            user=request.user,
            author=author)
        subscription.delete()
        response_data = {'detail': 'Вы отписались от автора.'}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            url_name='subscriptions',
            url_path='subscriptions',
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        """Метод запроса всех подписок модели пользователя."""

        queryset = Subscription.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(
            pages,
            many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)
