from django.db.models import Sum
from django.http import HttpResponse

from recipes.models import RecipeIngredientsAmount

FILENAME = 'shopping list'


def get_shopping_list_file(request):
    """Функция генерации тектового файла. Возвращает response
    в виде файла со списком ингредиентов, необходимых для приготовления
    рецептов, добавленных в список покупок."""

    shopping_list = "Cписок покупок:"
    ingredients = RecipeIngredientsAmount.objects.filter(
        recipe__shopping_cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
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
    ] = f'attachment; filename="{FILENAME}.txt"'
    return response
