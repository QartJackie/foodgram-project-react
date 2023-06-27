from django.db.models import Sum
from django.http import HttpResponse
from foodgram_backend.settings import UPLOAD_FILE_NAME
from recipes.models import RecipeIngredientsAmount


def convert_ingredient_data_for_create(self, ingredients, recipe):
    ingredient_list = []
    for ingredient in ingredients:
        ingredient_data = {}
        ingredient_data['ingredient_id'] = ingredient['id']
        ingredient_data['recipe_id'] = recipe.pk
        ingredient_data['amount'] = ingredient['amount']
        ingredient_list.append(
            ingredient_data
        )
    return ingredient_list


def get_shopping_list_file(request):
    """Функция генерации тектового файла. Возвращает response
    в виде файла со списком ингредиентов, необходимых для приготовления
    рецептов, добавленных в список покупок."""

    shopping_list = "Cписок покупок:"
    ingredients = RecipeIngredientsAmount.objects.filter(
        recipe__shopping_cart__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit').annotate(amount=Sum('amount'))
    for ingredient_number, ingredient in enumerate(ingredients):
        shopping_list += (
            f"\n{ingredient['ingredient__name']} - "
            f"{ingredient['amount']} "
            f"{ingredient['ingredient__measurement_unit']}"
        )
        if ingredient_number < ingredients.count() - 1:
            shopping_list += ','
    response = HttpResponse(
        shopping_list,
        content_type='text/plain'
    )
    response[
        'Content-Disposition'
    ] = f'attachment; filename="{UPLOAD_FILE_NAME}.txt"'
    return response
