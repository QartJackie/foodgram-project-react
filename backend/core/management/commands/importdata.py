import json
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Модель команды импорта ингридиентов."""

    def handle(self, *args, **options):
        """Реализация команды."""

        with open('core/data/ingredients.json', encoding='utf-8') as raw_data:
            print('Загрузка данных из файла.')
            jsondata = json.load(raw_data)
            print('Данные прочитаны.')
            print('Началась загрузка ингредиентов.')
            try:
                for ingredient in jsondata:
                    if not Ingredient.objects.filter(
                        name=ingredient['name'],
                        measurement_unit=ingredient['measurement_unit']
                    ).exists():
                        Ingredient.objects.create(
                            name=ingredient['name'],
                            measurement_unit=ingredient['measurement_unit'])
                ingredients_count = Ingredient.objects.all().count()
                print(f'{ingredients_count} ингрединетов импортировано.')
                print('Импорт завершен.')
            except Exception as error_message:
                raise Exception(error_message)
