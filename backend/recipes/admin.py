from django.contrib import admin

from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredientsAmount, ShoppingCart, Tag)


class TagAdmin(admin.ModelAdmin):
    """Модель админки тегов."""

    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )


class IngredientAdmin(admin.ModelAdmin):
    """Модель админки ингредиентов."""

    list_display = (
        'id',
        'name',
        'measurement_unit',
    )


class RecipeAdmin(admin.ModelAdmin):
    """Модель админки рецептов."""

    list_display = (
        'id',
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
        'create_at',
    )
    readonly_fields = ('added_to_favorites',)
    list_filter = (
        'name',
        'author',
        'tags',
    )
    search_fields = (
        'name',
        'create_at',
    )

    def added_to_favorites(self, recipe):
        return FavoriteRecipe.objects.filter(recipe=recipe).count()


class RecipeIngredientsAmountAdmin(admin.ModelAdmin):
    """Модель админки для вспомогательной модели
    с количеством ингридиентов."""

    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    """Модель админки списка покупок."""
    list_display = (
        'id',
        'recipe',
        'user',
        'create_at'
    )


class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Модель админки избранных рецептов."""
    list_display = (
        'id',
        'recipe',
        'user',
        'create_at',
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredientsAmount, RecipeIngredientsAmountAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
