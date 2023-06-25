# Generated by Django 3.2.3 on 2023-06-25 21:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления в избранное')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
                'ordering': ['-create_at'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Укажите название ингредиента', max_length=200, verbose_name='Название ингридиента')),
                ('measurement_unit', models.CharField(help_text='Укажите меру измерения, например граммы или литры', max_length=200, verbose_name='Мера измерения ингридиента')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Назовите рецепт', max_length=200, verbose_name='Название рецепта')),
                ('image', models.ImageField(help_text='Добавьте изображение готового блюда', upload_to='meal/images/', verbose_name='Фотография блюда')),
                ('text', models.TextField(help_text='Опишите процесс приготовления блюда', max_length=200, verbose_name='Описание рецепта')),
                ('cooking_time', models.IntegerField(help_text='Укажите время приготовления в минутах', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления (в минутах)')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-create_at'],
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredientsAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(help_text='Сколько ингредиента нужно добавить в соответствующей мере изменения?', validators=[django.core.validators.MinValueValidator(1, message='Нет ингредиентов - нет блюда!')], verbose_name='Необходимое количество ингредиента.')),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиенты в рецептах',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Укажите название тега', max_length=200, unique=True, verbose_name='Название тега')),
                ('color', models.CharField(help_text='Добавьте цвет тега в hex формате', max_length=16, verbose_name='Цвет тега')),
                ('slug', models.SlugField(help_text='Добавьте слаг', unique=True, verbose_name='Идентификатор тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления в покупки.')),
                ('recipe', models.ForeignKey(help_text='Выберите рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to='recipes.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
                'ordering': ['-create_at'],
            },
        ),
    ]