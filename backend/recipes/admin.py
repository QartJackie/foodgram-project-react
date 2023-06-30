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
    list_filter = ('name',)
    search_fields = ('name',)


class RecipeIngredients(admin.TabularInline):
    model = RecipeIngredientsAmount


class RecipeAdmin(admin.ModelAdmin):
    """Модель админки рецептов."""
    inlines = [RecipeIngredients, ]
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
        'create_at',
        'recipe_ingredients',
        'added_to_favorites',
    )
    readonly_fields = ('recipe_ingredients', 'added_to_favorites',)
    list_filter = (
        'name',
        'tags',
        'create_at',
    )
    search_fields = (
        'name',
        'author__email',
        'author__username',
        'author__first_name',
        'author__last_name',
        'tags__name',
        'tags__slug',
    )

    def added_to_favorites(self, recipe):
        return FavoriteRecipe.objects.filter(recipe=recipe).count()
    added_to_favorites.short_description = 'Добавлено в избранное раз'

    def recipe_ingredients(self, recipe):
        ingredient_list = []
        for ingredient in recipe.ingredients.all():
            ingredient_list.append(ingredient)
        return ingredient_list
    recipe_ingredients.short_description = 'Ингредиенты'


class RecipeIngredientsAmountAdmin(admin.ModelAdmin):
    """Модель админки для вспомогательной модели
    с количеством ингридиентов."""

    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )
    list_filter = ('recipe__tags', 'recipe__create_at')


class ShoppingCartAdmin(admin.ModelAdmin):
    """Модель админки списка покупок."""
    list_display = (
        'id',
        'recipe',
        'user',
        'create_at'
    )
    list_filter = (
        'recipe__tags',
        'recipe__create_at',
    )
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'recipe__name',
    )


class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Модель админки избранных рецептов."""
    list_display = (
        'id',
        'recipe',
        'user',
        'create_at',
    )
    list_filter = (
        'user',
        'recipe__tags',
        'recipe__create_at',
    )
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'recipe__name',
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredientsAmount, RecipeIngredientsAmountAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
