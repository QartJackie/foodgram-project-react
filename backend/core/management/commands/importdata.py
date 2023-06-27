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
                Ingredient.objects.bulk_create(
                    [Ingredient(**ingredient) for ingredient in jsondata]
                )
                print(f'{Ingredient.objects.all().count()} '
                      'ингрединетов импортировано.')
                print('Импорт завершен.')
            except Exception as error_message:
                raise Exception(error_message)
