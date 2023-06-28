# Generated by Django 3.2.3 on 2023-06-28 20:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipeingredientsamount',
            options={'ordering': ['recipe'], 'verbose_name': 'Ингредиент в рецепте', 'verbose_name_plural': 'Ингредиенты в рецептах'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.IntegerField(help_text='Укажите время приготовления в минутах', validators=[django.core.validators.MinValueValidator(1, message='Время приготовления должно быть больше 1')], verbose_name='Время приготовления (в минутах)'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Отметьте подходящие теги', related_name='recipe', to='recipes.Tag', verbose_name='Теги'),
        ),
    ]
