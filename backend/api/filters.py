from django_filters import rest_framework as filter
from recipes.models import Recipe, Tag
from rest_framework.filters import SearchFilter


class TagFilter(SearchFilter):
    """Фильтр тегов по имени."""
    search_param = 'name'


class IngredientFilter(SearchFilter):
    """Фильтр ингредиентов по имени."""
    search_param = 'name'


class RecipeFilter(filter.FilterSet):
    """Фильтр рецептов по автору, тегам, спискам покупок и избранного."""

    author = filter.CharFilter()
    tags = filter.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        label='Tags',
        to_field_name='slug',
    )

    is_favorited = filter.BooleanFilter(method='get_favorite')
    is_in_shopping_cart = filter.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart'
            )

    def get_favorite(self, queryset, name, value):
        """Метод получения списка рецептов
        избранного для текущего пользователя."""

        if value and self.request:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        """Метод получения рецептов, находящихся в
        списке покупок текущего пользователя."""

        if value and self.request:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
