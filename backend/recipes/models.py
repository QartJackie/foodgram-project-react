from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        'Название тега',
        max_length=200,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
        help_text='Укажите название тега',
    )
    color = models.CharField(
        'Цвет тега',
        max_length=16,
        blank=False,
        null=False,
        help_text='Добавьте цвет тега в hex формате',
    )
    slug = models.SlugField(
        'Идентификатор тега',
        unique=True,
        blank=False,
        null=False,
        help_text='Добавьте слаг',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    """Модель ингридиента."""
    name = models.CharField(
        'Название ингридиента',
        max_length=200,
        null=False,
        blank=False,
        db_index=True,
        help_text='Укажите название ингредиента'
    )
    measurement_unit = models.CharField(
        'Мера измерения ингридиента',
        max_length=200,
        blank=False,
        null=False,
        help_text='Укажите меру измерения, например граммы или литры',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_measurement',
            )
        ]

class Recipe(models.Model):
    """Модель рецепта."""

    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        verbose_name='Теги',
        help_text='Отметьте теги, подходящие Вашему блюду'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientsAmount',
        related_name='recipe',
        verbose_name='Ингредиенты',
        help_text='Добавьте необходимые ингредиенты',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        null=False,
        blank=False,
        help_text='Назовите рецепт',
    )
    image = models.ImageField(
        'Фотография блюда',
        upload_to='meal/images/',
        null=False,
        blank=False,
        help_text='Добавьте изображение готового блюда',
    )
    text = models.TextField(
        'Описание рецепта',
        max_length=200,
        null=False,
        blank=False,
        help_text='Опишите процесс приготовления блюда',
    )
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        null=False,
        blank=False,
        validators=[MinValueValidator(1)],
        help_text='Укажите время приготовления в минутах',
    )
    create_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['-create_at']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredientsAmount(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Ингредиент',
        help_text='Выберите ингредиент'
    )
    amount = models.IntegerField(
        'Необходимое количество ингредиента.',
        validators=[
            MinValueValidator(
                1,
                message='Нет ингредиентов - нет блюда!'
            )
        ],
        help_text='Сколько ингредиента нужно '
                  'добавить в соответствующей мере изменения?'
    )

    def __str__(self):
        return (f'Ингрединет: {self.ingredient.name}'
                f'из рецепта: {self.recipe.name}')

    class Meta:
        """Сортировка выдачи и проверка уникальности ингредиентов."""

        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredients',
            )
        ]
        ordering = ['-id']
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'


class ShoppingCart(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
        help_text='Выберите рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Покупатель',
    )
    create_at = models.DateTimeField(
        'Дата добавления в покупки.',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Рецепт "{self.recipe.name}" в покупках у {self.user}'

    class Meta:
        """Представление модели и валидация уникальности."""
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipes',
            )
        ]
        ordering = ['-create_at']
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'


class FavoriteRecipe(models.Model):
    """Модель избранных рецептов."""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранный рецепт',
        help_text='Выберите рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Автор подписки',
    )
    create_at = models.DateTimeField(
        'Дата добавления в избранное',
        auto_now_add=True
    )

    def __str__(self):
        return f'Рецепт "{self.recipe}" в избранном у {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite',
            )
        ]
        ordering = ['-create_at']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
